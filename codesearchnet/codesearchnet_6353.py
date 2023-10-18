def _model_to_sbml(cobra_model, f_replace=None, units=True):
    """Convert Cobra model to SBMLDocument.

    Parameters
    ----------
    cobra_model : cobra.core.Model
        Cobra model instance
    f_replace : dict of replacement functions
        Replacement to apply on identifiers.
    units : boolean
        Should the FLUX_UNITS be written in the SBMLDocument.

    Returns
    -------
    libsbml.SBMLDocument
    """
    if f_replace is None:
        f_replace = {}

    sbml_ns = libsbml.SBMLNamespaces(3, 1)  # SBML L3V1
    sbml_ns.addPackageNamespace("fbc", 2)  # fbc-v2

    doc = libsbml.SBMLDocument(sbml_ns)  # noqa: E501 type: libsbml.SBMLDocument
    doc.setPackageRequired("fbc", False)
    doc.setSBOTerm(SBO_FBA_FRAMEWORK)

    model = doc.createModel()  # type: libsbml.Model
    model_fbc = model.getPlugin("fbc")  # type: libsbml.FbcModelPlugin
    model_fbc.setStrict(True)

    if cobra_model.id is not None:
        model.setId(cobra_model.id)
        model.setMetaId("meta_" + cobra_model.id)
    else:
        model.setMetaId("meta_model")
    if cobra_model.name is not None:
        model.setName(cobra_model.name)

    _sbase_annotations(model, cobra_model.annotation)

    # Meta information (ModelHistory)
    if hasattr(cobra_model, "_sbml"):
        meta = cobra_model._sbml
        if "annotation" in meta:
            _sbase_annotations(doc, meta["annotation"])
        if "notes" in meta:
            _sbase_notes_dict(doc, meta["notes"])

        history = libsbml.ModelHistory()  # type: libsbml.ModelHistory
        if "created" in meta and meta["created"]:
            history.setCreatedDate(meta["created"])
        else:
            time = datetime.datetime.now()
            timestr = time.strftime('%Y-%m-%dT%H:%M:%S')
            date = libsbml.Date(timestr)
            _check(history.setCreatedDate(date), 'set creation date')
            _check(history.setModifiedDate(date), 'set modified date')

        if "creators" in meta:
            for cobra_creator in meta["creators"]:
                creator = libsbml.ModelCreator()  # noqa: E501 type: libsbml.ModelCreator
                if cobra_creator.get("familyName", None):
                    creator.setFamilyName(cobra_creator["familyName"])
                if cobra_creator.get("givenName", None):
                    creator.setGivenName(cobra_creator["givenName"])
                if cobra_creator.get("organisation", None):
                    creator.setOrganisation(cobra_creator["organisation"])
                if cobra_creator.get("email", None):
                    creator.setEmail(cobra_creator["email"])

                _check(history.addCreator(creator),
                       "adding creator to ModelHistory.")
        _check(model.setModelHistory(history), 'set model history')

    # Units
    if units:
        flux_udef = model.createUnitDefinition()  # noqa: E501 type: libsbml.UnitDefinition
        flux_udef.setId(UNITS_FLUX[0])
        for u in UNITS_FLUX[1]:
            unit = flux_udef.createUnit()  # type: libsbml.Unit
            unit.setKind(u.kind)
            unit.setExponent(u.exponent)
            unit.setScale(u.scale)
            unit.setMultiplier(u.multiplier)

    # minimum and maximum value from model
    if len(cobra_model.reactions) > 0:
        min_value = min(cobra_model.reactions.list_attr("lower_bound"))
        max_value = max(cobra_model.reactions.list_attr("upper_bound"))
    else:
        min_value = config.lower_bound
        max_value = config.upper_bound

    _create_parameter(model, pid=LOWER_BOUND_ID,
                      value=min_value, sbo=SBO_DEFAULT_FLUX_BOUND)
    _create_parameter(model, pid=UPPER_BOUND_ID,
                      value=max_value, sbo=SBO_DEFAULT_FLUX_BOUND)
    _create_parameter(model, pid=ZERO_BOUND_ID,
                      value=0, sbo=SBO_DEFAULT_FLUX_BOUND)
    _create_parameter(model, pid=BOUND_MINUS_INF,
                      value=-float("Inf"), sbo=SBO_FLUX_BOUND)
    _create_parameter(model, pid=BOUND_PLUS_INF,
                      value=float("Inf"), sbo=SBO_FLUX_BOUND)

    # Compartments
    # FIXME: use first class compartment model (and write notes & annotations)
    #     (https://github.com/opencobra/cobrapy/issues/811)
    for cid, name in iteritems(cobra_model.compartments):
        compartment = model.createCompartment()  # type: libsbml.Compartment
        compartment.setId(cid)
        compartment.setName(name)
        compartment.setConstant(True)

        # FIXME: write annotations and notes
        # _sbase_notes(c, com.notes)
        # _sbase_annotations(c, com.annotation)

    # Species
    for metabolite in cobra_model.metabolites:
        specie = model.createSpecies()  # type: libsbml.Species
        mid = metabolite.id
        if f_replace and F_SPECIE_REV in f_replace:
            mid = f_replace[F_SPECIE_REV](mid)
        specie.setId(mid)
        specie.setConstant(False)
        specie.setBoundaryCondition(False)
        specie.setHasOnlySubstanceUnits(False)
        specie.setName(metabolite.name)
        specie.setCompartment(metabolite.compartment)
        s_fbc = specie.getPlugin("fbc")  # type: libsbml.FbcSpeciesPlugin
        if metabolite.charge is not None:
            s_fbc.setCharge(metabolite.charge)
        if metabolite.formula is not None:
            s_fbc.setChemicalFormula(metabolite.formula)

        _sbase_annotations(specie, metabolite.annotation)
        _sbase_notes_dict(specie, metabolite.notes)

    # Genes
    for cobra_gene in cobra_model.genes:
        gp = model_fbc.createGeneProduct()  # type: libsbml.GeneProduct
        gid = cobra_gene.id
        if f_replace and F_GENE_REV in f_replace:
            gid = f_replace[F_GENE_REV](gid)
        gp.setId(gid)
        gname = cobra_gene.name
        if gname is None or len(gname) == 0:
            gname = gid
        gp.setName(gname)
        gp.setLabel(gid)

        _sbase_annotations(gp, cobra_gene.annotation)
        _sbase_notes_dict(gp, cobra_gene.notes)

    # Objective
    objective = model_fbc.createObjective()  # type: libsbml.Objective
    objective.setId("obj")
    objective.setType(SHORT_LONG_DIRECTION[cobra_model.objective.direction])
    model_fbc.setActiveObjectiveId("obj")

    # Reactions
    reaction_coefficients = linear_reaction_coefficients(cobra_model)
    for cobra_reaction in cobra_model.reactions:
        rid = cobra_reaction.id
        if f_replace and F_REACTION_REV in f_replace:
            rid = f_replace[F_REACTION_REV](rid)
        reaction = model.createReaction()  # type: libsbml.Reaction
        reaction.setId(rid)
        reaction.setName(cobra_reaction.name)
        reaction.setFast(False)
        reaction.setReversible((cobra_reaction.lower_bound < 0))
        _sbase_annotations(reaction, cobra_reaction.annotation)
        _sbase_notes_dict(reaction, cobra_reaction.notes)

        # stoichiometry
        for metabolite, stoichiometry in iteritems(cobra_reaction._metabolites):  # noqa: E501
            sid = metabolite.id
            if f_replace and F_SPECIE_REV in f_replace:
                sid = f_replace[F_SPECIE_REV](sid)
            if stoichiometry < 0:
                sref = reaction.createReactant()  # noqa: E501 type: libsbml.SpeciesReference
                sref.setSpecies(sid)
                sref.setStoichiometry(-stoichiometry)
                sref.setConstant(True)
            else:
                sref = reaction.createProduct()  # noqa: E501 type: libsbml.SpeciesReference
                sref.setSpecies(sid)
                sref.setStoichiometry(stoichiometry)
                sref.setConstant(True)

        # bounds
        r_fbc = reaction.getPlugin("fbc")  # type: libsbml.FbcReactionPlugin
        r_fbc.setLowerFluxBound(_create_bound(model, cobra_reaction,
                                              "lower_bound",
                                              f_replace=f_replace, units=units,
                                              flux_udef=flux_udef))
        r_fbc.setUpperFluxBound(_create_bound(model, cobra_reaction,
                                              "upper_bound",
                                              f_replace=f_replace, units=units,
                                              flux_udef=flux_udef))

        # GPR
        gpr = cobra_reaction.gene_reaction_rule
        if gpr is not None and len(gpr) > 0:

            # replace ids in string
            if f_replace and F_GENE_REV in f_replace:
                gpr = gpr.replace('(', '( ')
                gpr = gpr.replace(')', ' )')
                tokens = gpr.split(' ')
                for k in range(len(tokens)):
                    if tokens[k] not in [' ', 'and', 'or', '(', ')']:
                        tokens[k] = f_replace[F_GENE_REV](tokens[k])
                gpr_new = " ".join(tokens)

            gpa = r_fbc.createGeneProductAssociation()  # noqa: E501 type: libsbml.GeneProductAssociation
            gpa.setAssociation(gpr_new)

        # objective coefficients
        if reaction_coefficients.get(cobra_reaction, 0) != 0:
            flux_obj = objective.createFluxObjective()  # noqa: E501 type: libsbml.FluxObjective
            flux_obj.setReaction(rid)
            flux_obj.setCoefficient(cobra_reaction.objective_coefficient)

    # write groups
    if len(cobra_model.groups) > 0:
        doc.enablePackage(
            "http://www.sbml.org/sbml/level3/version1/groups/version1",
            "groups", True)
        doc.setPackageRequired("groups", False)
        model_group = model.getPlugin("groups")  # noqa: E501 type: libsbml.GroupsModelPlugin
        for cobra_group in cobra_model.groups:
            group = model_group.createGroup()  # type: libsbml.Group
            group.setId(cobra_group.id)
            group.setName(cobra_group.name)
            group.setKind(cobra_group.kind)

            _sbase_notes_dict(group, cobra_group.notes)
            _sbase_annotations(group, cobra_group.annotation)

            for cobra_member in cobra_group.members:
                member = group.createMember()  # type: libsbml.Member
                mid = cobra_member.id
                m_type = str(type(cobra_member))

                # id replacements
                if "Reaction" in m_type:
                    if f_replace and F_REACTION_REV in f_replace:
                        mid = f_replace[F_REACTION_REV](mid)
                if "Metabolite" in m_type:
                    if f_replace and F_SPECIE_REV in f_replace:
                        mid = f_replace[F_SPECIE_REV](mid)
                if "Gene" in m_type:
                    if f_replace and F_GENE_REV in f_replace:
                        mid = f_replace[F_GENE_REV](mid)

                member.setIdRef(mid)
                if cobra_member.name and len(cobra_member.name) > 0:
                    member.setName(cobra_member.name)

    return doc