def create_mat_dict(model):
    """create a dict mapping model attributes to arrays"""
    rxns = model.reactions
    mets = model.metabolites
    mat = OrderedDict()
    mat["mets"] = _cell([met_id for met_id in create_mat_metabolite_id(model)])
    mat["metNames"] = _cell(mets.list_attr("name"))
    mat["metFormulas"] = _cell([str(m.formula) for m in mets])
    try:
        mat["metCharge"] = array(mets.list_attr("charge")) * 1.
    except TypeError:
        # can't have any None entries for charge, or this will fail
        pass
    mat["genes"] = _cell(model.genes.list_attr("id"))
    # make a matrix for rxnGeneMat
    # reactions are rows, genes are columns
    rxn_gene = scipy_sparse.dok_matrix((len(model.reactions),
                                        len(model.genes)))
    if min(rxn_gene.shape) > 0:
        for i, reaction in enumerate(model.reactions):
            for gene in reaction.genes:
                rxn_gene[i, model.genes.index(gene)] = 1
        mat["rxnGeneMat"] = rxn_gene
    mat["grRules"] = _cell(rxns.list_attr("gene_reaction_rule"))
    mat["rxns"] = _cell(rxns.list_attr("id"))
    mat["rxnNames"] = _cell(rxns.list_attr("name"))
    mat["subSystems"] = _cell(rxns.list_attr("subsystem"))
    stoich_mat = create_stoichiometric_matrix(model)
    mat["S"] = stoich_mat if stoich_mat is not None else [[]]
    # multiply by 1 to convert to float, working around scipy bug
    # https://github.com/scipy/scipy/issues/4537
    mat["lb"] = array(rxns.list_attr("lower_bound")) * 1.
    mat["ub"] = array(rxns.list_attr("upper_bound")) * 1.
    mat["b"] = array(mets.list_attr("_bound")) * 1.
    mat["c"] = array(rxns.list_attr("objective_coefficient")) * 1.
    mat["rev"] = array(rxns.list_attr("reversibility")) * 1
    mat["description"] = str(model.id)
    return mat