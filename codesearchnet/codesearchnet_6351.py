def _sbml_to_model(doc, number=float, f_replace=F_REPLACE,
                   set_missing_bounds=False, **kwargs):
    """Creates cobra model from SBMLDocument.

    Parameters
    ----------
    doc: libsbml.SBMLDocument
    number: data type of stoichiometry: {float, int}
        In which data type should the stoichiometry be parsed.
    f_replace : dict of replacement functions for id replacement
    set_missing_bounds : flag to set missing bounds

    Returns
    -------
    cobra.core.Model
    """
    if f_replace is None:
        f_replace = {}

    # SBML model
    model = doc.getModel()  # type: libsbml.Model
    if model is None:
        raise CobraSBMLError("No SBML model detected in file.")
    model_fbc = model.getPlugin("fbc")  # type: libsbml.FbcModelPlugin

    if not model_fbc:
        LOGGER.warning("Model does not contain SBML fbc package information.")
    else:
        if not model_fbc.isSetStrict():
            LOGGER.warning('Loading SBML model without fbc:strict="true"')

        # fbc-v1 (legacy)
        doc_fbc = doc.getPlugin("fbc")  # type: libsbml.FbcSBMLDocumentPlugin
        fbc_version = doc_fbc.getPackageVersion()

        if fbc_version == 1:
            LOGGER.warning("Loading SBML with fbc-v1 (models should be encoded"
                           " using fbc-v2)")
            conversion_properties = libsbml.ConversionProperties()
            conversion_properties.addOption("convert fbc v1 to fbc v2", True,
                                            "Convert FBC-v1 model to FBC-v2")
            result = doc.convert(conversion_properties)
            if result != libsbml.LIBSBML_OPERATION_SUCCESS:
                raise Exception("Conversion of SBML fbc v1 to fbc v2 failed")

    # Model
    cobra_model = Model(model.getId())
    cobra_model.name = model.getName()

    # meta information
    meta = {
        "model.id": model.getId(),
        "level": model.getLevel(),
        "version": model.getVersion(),
        "packages": []
    }
    # History
    creators = []
    created = None
    if model.isSetModelHistory():
        history = model.getModelHistory()  # type: libsbml.ModelHistory

        if history.isSetCreatedDate():
            created = history.getCreatedDate()

        for c in history.getListCreators():  # type: libsbml.ModelCreator
            creators.append({
                "familyName": c.getFamilyName() if c.isSetFamilyName() else None,  # noqa: E501
                "givenName": c.getGivenName() if c.isSetGivenName() else None,
                "organisation": c.getOrganisation() if c.isSetOrganisation() else None,  # noqa: E501
                "email": c.getEmail() if c.isSetEmail() else None,
            })

    meta["creators"] = creators
    meta["created"] = created
    meta["notes"] = _parse_notes_dict(doc)
    meta["annotation"] = _parse_annotations(doc)

    info = "<{}> SBML L{}V{}".format(model.getId(),
                                     model.getLevel(), model.getVersion())
    packages = {}
    for k in range(doc.getNumPlugins()):
        plugin = doc.getPlugin(k)  # type:libsbml.SBasePlugin
        key, value = plugin.getPackageName(), plugin.getPackageVersion()
        packages[key] = value
        info += ", {}-v{}".format(key, value)
        if key not in ["fbc", "groups"]:
            LOGGER.warning("SBML package '%s' not supported by cobrapy,"
                           "information is not parsed", key)
    meta["info"] = info
    meta["packages"] = packages
    cobra_model._sbml = meta

    # notes and annotations
    cobra_model.notes = _parse_notes_dict(model)
    cobra_model.annotation = _parse_annotations(model)

    # Compartments
    # FIXME: update with new compartments
    cobra_model.compartments = {c.getId(): c.getName()
                                for c in model.getListOfCompartments()}

    # Species
    metabolites = []
    boundary_metabolites = []
    if model.getNumSpecies() == 0:
        LOGGER.warning("No metabolites in model")

    for specie in model.getListOfSpecies():  # type: libsbml.Species
        sid = _check_required(specie, specie.getId(), "id")
        if f_replace and F_SPECIE in f_replace:
            sid = f_replace[F_SPECIE](sid)

        met = Metabolite(sid)
        met.name = specie.getName()
        met.notes = _parse_notes_dict(specie)
        met.annotation = _parse_annotations(specie)
        met.compartment = specie.getCompartment()

        specie_fbc = specie.getPlugin("fbc")  # type: libsbml.FbcSpeciesPlugin
        if specie_fbc:
            met.charge = specie_fbc.getCharge()
            met.formula = specie_fbc.getChemicalFormula()
        else:
            if specie.isSetCharge():
                LOGGER.warning("Use of the species charge attribute is "
                               "discouraged, use fbc:charge "
                               "instead: %s", specie)
                met.charge = specie.getCharge()
            else:
                if 'CHARGE' in met.notes:
                    LOGGER.warning("Use of CHARGE in the notes element is "
                                   "discouraged, use fbc:charge "
                                   "instead: %s", specie)
                    try:
                        met.charge = int(met.notes['CHARGE'])
                    except ValueError:
                        # handle nan, na, NA, ...
                        pass

            if 'FORMULA' in met.notes:
                LOGGER.warning("Use of FORMULA in the notes element is "
                               "discouraged, use fbc:chemicalFormula "
                               "instead: %s", specie)
                met.formula = met.notes['FORMULA']

        # Detect boundary metabolites
        if specie.getBoundaryCondition() is True:
            boundary_metabolites.append(met)

        metabolites.append(met)

    cobra_model.add_metabolites(metabolites)

    # Add exchange reactions for boundary metabolites
    ex_reactions = []
    for met in boundary_metabolites:
        ex_rid = "EX_{}".format(met.id)
        ex_reaction = Reaction(ex_rid)
        ex_reaction.name = ex_rid
        ex_reaction.annotation = {
            'sbo': SBO_EXCHANGE_REACTION
        }
        ex_reaction.lower_bound = -float("Inf")
        ex_reaction.upper_bound = float("Inf")
        LOGGER.warning("Adding exchange reaction %s for boundary metabolite: "
                       "%s" % (ex_reaction.id, met.id))
        # species is reactant
        ex_reaction.add_metabolites({met: -1})
        ex_reactions.append(ex_reaction)
    cobra_model.add_reactions(ex_reactions)

    # Genes
    if model_fbc:
        for gp in model_fbc.getListOfGeneProducts():  # noqa: E501 type: libsbml.GeneProduct
            gid = gp.getId()
            if f_replace and F_GENE in f_replace:
                gid = f_replace[F_GENE](gid)
            cobra_gene = Gene(gid)
            cobra_gene.name = gp.getName()
            if cobra_gene.name is None:
                cobra_gene.name = gid
            cobra_gene.annotation = _parse_annotations(gp)
            cobra_gene.notes = _parse_notes_dict(gp)

            cobra_model.genes.append(cobra_gene)
    else:
        for cobra_reaction in model.getListOfReactions():  # noqa: E501 type: libsbml.Reaction
            # fallback to notes information
            notes = _parse_notes_dict(cobra_reaction)
            if "GENE ASSOCIATION" in notes:
                gpr = notes['GENE ASSOCIATION']
            elif "GENE_ASSOCIATION" in notes:
                gpr = notes['GENE_ASSOCIATION']
            else:
                gpr = ''

            if len(gpr) > 0:
                gpr = gpr.replace("(", ";")
                gpr = gpr.replace(")", ";")
                gpr = gpr.replace("or", ";")
                gpr = gpr.replace("and", ";")
                gids = [t.strip() for t in gpr.split(';')]

                # create missing genes
                for gid in gids:
                    if f_replace and F_GENE in f_replace:
                        gid = f_replace[F_GENE](gid)

                    if gid not in cobra_model.genes:
                        cobra_gene = Gene(gid)
                        cobra_gene.name = gid
                        cobra_model.genes.append(cobra_gene)

    # GPR rules
    def process_association(ass):
        """ Recursively convert gpr association to a gpr string.
        Defined as inline functions to not pass the replacement dict around.
        """
        if ass.isFbcOr():
            return " ".join(
                ["(", ' or '.join(process_association(c)
                                  for c in ass.getListOfAssociations()), ")"]
            )
        elif ass.isFbcAnd():
            return " ".join(
                ["(", ' and '.join(process_association(c)
                                   for c in ass.getListOfAssociations()), ")"])
        elif ass.isGeneProductRef():
            gid = ass.getGeneProduct()
            if f_replace and F_GENE in f_replace:
                return f_replace[F_GENE](gid)
            else:
                return gid

    # Reactions
    missing_bounds = False
    reactions = []
    if model.getNumReactions() == 0:
        LOGGER.warning("No reactions in model")

    for reaction in model.getListOfReactions():  # type: libsbml.Reaction
        rid = _check_required(reaction, reaction.getId(), "id")
        if f_replace and F_REACTION in f_replace:
            rid = f_replace[F_REACTION](rid)
        cobra_reaction = Reaction(rid)
        cobra_reaction.name = reaction.getName()
        cobra_reaction.annotation = _parse_annotations(reaction)
        cobra_reaction.notes = _parse_notes_dict(reaction)

        # set bounds
        p_ub, p_lb = None, None
        r_fbc = reaction.getPlugin("fbc")  # type: libsbml.FbcReactionPlugin
        if r_fbc:
            # bounds in fbc
            lb_id = r_fbc.getLowerFluxBound()
            if lb_id:
                p_lb = model.getParameter(lb_id)  # type: libsbml.Parameter
                if p_lb and p_lb.getConstant() and \
                        (p_lb.getValue() is not None):
                    cobra_reaction.lower_bound = p_lb.getValue()
                else:
                    raise CobraSBMLError("No constant bound '%s' for "
                                         "reaction: %s" % (p_lb, reaction))

            ub_id = r_fbc.getUpperFluxBound()
            if ub_id:
                p_ub = model.getParameter(ub_id)  # type: libsbml.Parameter
                if p_ub and p_ub.getConstant() and \
                        (p_ub.getValue() is not None):
                    cobra_reaction.upper_bound = p_ub.getValue()
                else:
                    raise CobraSBMLError("No constant bound '%s' for "
                                         "reaction: %s" % (p_ub, reaction))

        elif reaction.isSetKineticLaw():
            # some legacy models encode bounds in kinetic laws
            klaw = reaction.getKineticLaw()  # type: libsbml.KineticLaw
            p_lb = klaw.getParameter("LOWER_BOUND")  # noqa: E501 type: libsbml.LocalParameter
            if p_lb:
                cobra_reaction.lower_bound = p_lb.getValue()
            p_ub = klaw.getParameter("UPPER_BOUND")  # noqa: E501 type: libsbml.LocalParameter
            if p_ub:
                cobra_reaction.upper_bound = p_ub.getValue()

            if p_ub is not None or p_lb is not None:
                LOGGER.warning("Encoding LOWER_BOUND and UPPER_BOUND in "
                               "KineticLaw is discouraged, "
                               "use fbc:fluxBounds instead: %s", reaction)

        if p_lb is None:
            missing_bounds = True
            if set_missing_bounds:
                lower_bound = config.lower_bound
            else:
                lower_bound = -float("Inf")
            cobra_reaction.lower_bound = lower_bound
            LOGGER.warning("Missing lower flux bound set to '%s' for "
                           " reaction: '%s'", lower_bound, reaction)

        if p_ub is None:
            missing_bounds = True
            if set_missing_bounds:
                upper_bound = config.upper_bound
            else:
                upper_bound = float("Inf")
            cobra_reaction.upper_bound = upper_bound
            LOGGER.warning("Missing upper flux bound set to '%s' for "
                           " reaction: '%s'", upper_bound, reaction)

        # add reaction
        reactions.append(cobra_reaction)

        # parse equation
        stoichiometry = defaultdict(lambda: 0)
        for sref in reaction.getListOfReactants():  # noqa: E501 type: libsbml.SpeciesReference
            sid = sref.getSpecies()
            if f_replace and F_SPECIE in f_replace:
                sid = f_replace[F_SPECIE](sid)
            stoichiometry[sid] -= number(
                _check_required(sref, sref.getStoichiometry(),
                                "stoichiometry"))

        for sref in reaction.getListOfProducts():  # noqa: E501 type: libsbml.SpeciesReference
            sid = sref.getSpecies()
            if f_replace and F_SPECIE in f_replace:
                sid = f_replace[F_SPECIE](sid)
            stoichiometry[sid] += number(
                _check_required(sref, sref.getStoichiometry(),
                                "stoichiometry"))

        # convert to metabolite objects
        object_stoichiometry = {}
        for met_id in stoichiometry:
            metabolite = cobra_model.metabolites.get_by_id(met_id)
            object_stoichiometry[metabolite] = stoichiometry[met_id]
        cobra_reaction.add_metabolites(object_stoichiometry)

        # GPR
        if r_fbc:
            gpr = ''
            gpa = r_fbc.getGeneProductAssociation()  # noqa: E501 type: libsbml.GeneProductAssociation
            if gpa is not None:
                association = gpa.getAssociation()  # noqa: E501 type: libsbml.FbcAssociation
                gpr = process_association(association)
        else:
            # fallback to notes information
            notes = cobra_reaction.notes
            if "GENE ASSOCIATION" in notes:
                gpr = notes['GENE ASSOCIATION']
            elif "GENE_ASSOCIATION" in notes:
                gpr = notes['GENE_ASSOCIATION']
            else:
                gpr = ''

            if len(gpr) > 0:
                LOGGER.warning("Use of GENE ASSOCIATION or GENE_ASSOCIATION "
                               "in the notes element is discouraged, use "
                               "fbc:gpr instead: %s", reaction)
                if f_replace and F_GENE in f_replace:
                    gpr = " ".join(
                        f_replace[F_GENE](t) for t in gpr.split(' ')
                    )

        # remove outside parenthesis, if any
        if gpr.startswith("(") and gpr.endswith(")"):
            gpr = gpr[1:-1].strip()

        cobra_reaction.gene_reaction_rule = gpr

    cobra_model.add_reactions(reactions)

    # Objective
    obj_direction = "max"
    coefficients = {}
    if model_fbc:
        obj_list = model_fbc.getListOfObjectives()  # noqa: E501 type: libsbml.ListOfObjectives
        if obj_list is None:
            LOGGER.warning("listOfObjectives element not found")
        elif obj_list.size() == 0:
            LOGGER.warning("No objective in listOfObjectives")
        elif not obj_list.getActiveObjective():
            LOGGER.warning("No active objective in listOfObjectives")
        else:
            obj_id = obj_list.getActiveObjective()
            obj = model_fbc.getObjective(obj_id)  # type: libsbml.Objective
            obj_direction = LONG_SHORT_DIRECTION[obj.getType()]

            for flux_obj in obj.getListOfFluxObjectives():  # noqa: E501 type: libsbml.FluxObjective
                rid = flux_obj.getReaction()
                if f_replace and F_REACTION in f_replace:
                    rid = f_replace[F_REACTION](rid)
                try:
                    objective_reaction = cobra_model.reactions.get_by_id(rid)
                except KeyError:
                    raise CobraSBMLError("Objective reaction '%s' "
                                         "not found" % rid)
                try:
                    coefficients[objective_reaction] = number(
                        flux_obj.getCoefficient()
                    )
                except ValueError as e:
                    LOGGER.warning(str(e))
    else:
        # some legacy models encode objective coefficients in kinetic laws
        for reaction in model.getListOfReactions():  # noqa: E501 type: libsbml.Reaction
            if reaction.isSetKineticLaw():
                klaw = reaction.getKineticLaw()  # type: libsbml.KineticLaw
                p_oc = klaw.getParameter(
                    "OBJECTIVE_COEFFICIENT")  # noqa: E501 type: libsbml.LocalParameter
                if p_oc:
                    rid = reaction.getId()
                    if f_replace and F_REACTION in f_replace:
                        rid = f_replace[F_REACTION](rid)
                    try:
                        objective_reaction = cobra_model.reactions.get_by_id(
                            rid)
                    except KeyError:
                        raise CobraSBMLError("Objective reaction '%s' "
                                             "not found", rid)
                    try:
                        coefficients[objective_reaction] = number(
                            p_oc.getValue())
                    except ValueError as e:
                        LOGGER.warning(str(e))

                    LOGGER.warning("Encoding OBJECTIVE_COEFFICIENT in "
                                   "KineticLaw is discouraged, "
                                   "use fbc:fluxObjective "
                                   "instead: %s", cobra_reaction)

    if len(coefficients) == 0:
        LOGGER.error("No objective coefficients in model. Unclear what should "
                     "be optimized")
    set_objective(cobra_model, coefficients)
    cobra_model.solver.objective.direction = obj_direction

    # parse groups
    model_groups = model.getPlugin("groups")  # type: libsbml.GroupsModelPlugin
    groups = []
    if model_groups:
        # calculate hashmaps to lookup objects in O(1)
        sid_map = {}
        metaid_map = {}
        for obj_list in [model.getListOfCompartments(),
                         model.getListOfSpecies(),
                         model.getListOfReactions(),
                         model_groups.getListOfGroups()]:

            for sbase in obj_list:  # type: libsbml.SBase
                if sbase.isSetId():
                    sid_map[sbase.getId()] = sbase
                if sbase.isSetMetaId():
                    metaid_map[sbase.getMetaId()] = sbase

        # create groups
        for group in model_groups.getListOfGroups():  # type: libsbml.Group
            cobra_group = Group(group.getId())
            cobra_group.name = group.getName()
            if group.isSetKind():
                cobra_group.kind = group.getKindAsString()
            cobra_group.annotation = _parse_annotations(group)
            cobra_group.notes = _parse_notes_dict(group)

            cobra_members = []
            for member in group.getListOfMembers():  # type: libsbml.Member
                if member.isSetIdRef():
                    obj = sid_map[member.getIdRef()]
                    # obj = doc.getElementBySId(member.getIdRef())
                elif member.isSetMetaIdRef():
                    obj = metaid_map[member.getMetaIdRef()]
                    # obj = doc.getElementByMetaId(member.getMetaIdRef())

                typecode = obj.getTypeCode()
                obj_id = obj.getId()

                # id replacements
                cobra_member = None
                if typecode == libsbml.SBML_SPECIES:
                    if f_replace and F_SPECIE in f_replace:
                        obj_id = f_replace[F_SPECIE](obj_id)
                    cobra_member = cobra_model.metabolites.get_by_id(obj_id)
                elif typecode == libsbml.SBML_REACTION:
                    if f_replace and F_REACTION in f_replace:
                        obj_id = f_replace[F_REACTION](obj_id)
                    cobra_member = cobra_model.reactions.get_by_id(obj_id)
                elif typecode == libsbml.SBML_FBC_GENEPRODUCT:
                    if f_replace and F_GENE in f_replace:
                        obj_id = f_replace[F_GENE](obj_id)
                    cobra_member = cobra_model.genes.get_by_id(obj_id)
                else:
                    LOGGER.warning("Member %s could not be added to group %s."
                                   "unsupported type code: "
                                   "%s" % (member, group, typecode))

                if cobra_member:
                    cobra_members.append(cobra_member)

            cobra_group.add_members(cobra_members)
            groups.append(cobra_group)
    else:
        # parse deprecated subsystems on reactions
        groups_dict = {}
        for cobra_reaction in cobra_model.reactions:
            if "SUBSYSTEM" in cobra_reaction.notes:
                g_name = cobra_reaction.notes["SUBSYSTEM"]
                if g_name in groups_dict:
                    groups_dict[g_name].append(cobra_reaction)
                else:
                    groups_dict[g_name] = [cobra_reaction]

        for gid, cobra_members in groups_dict.items():
            cobra_group = Group(gid, name=gid, kind="collection")
            cobra_group.add_members(cobra_members)
            groups.append(cobra_group)

    cobra_model.add_groups(groups)

    # general hint for missing flux bounds
    if missing_bounds and not set_missing_bounds:
        LOGGER.warning("Missing flux bounds on reactions. As best practise "
                       "and to avoid confusion flux bounds should be set "
                       "explicitly on all reactions. "
                       "To set the missing flux bounds to default bounds "
                       "specified in cobra.Configuration use the flag "
                       "`read_sbml_model(..., set_missing_bounds=True)`.")

    return cobra_model