def from_mat_struct(mat_struct, model_id=None, inf=inf):
    """create a model from the COBRA toolbox struct

    The struct will be a dict read in by scipy.io.loadmat

    """
    m = mat_struct
    if m.dtype.names is None:
        raise ValueError("not a valid mat struct")
    if not {"rxns", "mets", "S", "lb", "ub"} <= set(m.dtype.names):
        raise ValueError("not a valid mat struct")
    if "c" in m.dtype.names:
        c_vec = m["c"][0, 0]
    else:
        c_vec = None
        warn("objective vector 'c' not found")
    model = Model()
    if model_id is not None:
        model.id = model_id
    elif "description" in m.dtype.names:
        description = m["description"][0, 0][0]
        if not isinstance(description, string_types) and len(description) > 1:
            model.id = description[0]
            warn("Several IDs detected, only using the first.")
        else:
            model.id = description
    else:
        model.id = "imported_model"
    for i, name in enumerate(m["mets"][0, 0]):
        new_metabolite = Metabolite()
        new_metabolite.id = str(name[0][0])
        if all(var in m.dtype.names for var in
               ['metComps', 'comps', 'compNames']):
            comp_index = m["metComps"][0, 0][i][0] - 1
            new_metabolite.compartment = m['comps'][0, 0][comp_index][0][0]
            if new_metabolite.compartment not in model.compartments:
                comp_name = m['compNames'][0, 0][comp_index][0][0]
                model.compartments[new_metabolite.compartment] = comp_name
        else:
            new_metabolite.compartment = _get_id_compartment(new_metabolite.id)
            if new_metabolite.compartment not in model.compartments:
                model.compartments[
                    new_metabolite.compartment] = new_metabolite.compartment
        try:
            new_metabolite.name = str(m["metNames"][0, 0][i][0][0])
        except (IndexError, ValueError):
            pass
        try:
            new_metabolite.formula = str(m["metFormulas"][0][0][i][0][0])
        except (IndexError, ValueError):
            pass
        try:
            new_metabolite.charge = float(m["metCharge"][0, 0][i][0])
            int_charge = int(new_metabolite.charge)
            if new_metabolite.charge == int_charge:
                new_metabolite.charge = int_charge
        except (IndexError, ValueError):
            pass
        model.add_metabolites([new_metabolite])
    new_reactions = []
    coefficients = {}
    for i, name in enumerate(m["rxns"][0, 0]):
        new_reaction = Reaction()
        new_reaction.id = str(name[0][0])
        new_reaction.lower_bound = float(m["lb"][0, 0][i][0])
        new_reaction.upper_bound = float(m["ub"][0, 0][i][0])
        if isinf(new_reaction.lower_bound) and new_reaction.lower_bound < 0:
            new_reaction.lower_bound = -inf
        if isinf(new_reaction.upper_bound) and new_reaction.upper_bound > 0:
            new_reaction.upper_bound = inf
        if c_vec is not None:
            coefficients[new_reaction] = float(c_vec[i][0])
        try:
            new_reaction.gene_reaction_rule = str(m['grRules'][0, 0][i][0][0])
        except (IndexError, ValueError):
            pass
        try:
            new_reaction.name = str(m["rxnNames"][0, 0][i][0][0])
        except (IndexError, ValueError):
            pass
        try:
            new_reaction.subsystem = str(m['subSystems'][0, 0][i][0][0])
        except (IndexError, ValueError):
            pass
        new_reactions.append(new_reaction)
    model.add_reactions(new_reactions)
    set_objective(model, coefficients)
    coo = scipy_sparse.coo_matrix(m["S"][0, 0])
    for i, j, v in zip(coo.row, coo.col, coo.data):
        model.reactions[j].add_metabolites({model.metabolites[i]: v})
    return model