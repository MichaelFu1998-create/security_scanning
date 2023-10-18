def add_mip_obj(model):
    """Add a mixed-integer version of a minimal medium to the model.

    Changes the optimization objective to finding the medium with the least
    components::

        minimize size(R) where R part of import_reactions

    Arguments
    ---------
    model : cobra.model
        The model to modify.
    """
    if len(model.variables) > 1e4:
        LOGGER.warning("the MIP version of minimal media is extremely slow for"
                       " models that large :(")
    exchange_rxns = find_boundary_types(model, "exchange")
    big_m = max(abs(b) for r in exchange_rxns for b in r.bounds)
    prob = model.problem
    coefs = {}
    to_add = []
    for rxn in exchange_rxns:
        export = len(rxn.reactants) == 1
        indicator = prob.Variable("ind_" + rxn.id, lb=0, ub=1, type="binary")
        if export:
            vrv = rxn.reverse_variable
            indicator_const = prob.Constraint(
                vrv - indicator * big_m, ub=0, name="ind_constraint_" + rxn.id)
        else:
            vfw = rxn.forward_variable
            indicator_const = prob.Constraint(
                vfw - indicator * big_m, ub=0, name="ind_constraint_" + rxn.id)
        to_add.extend([indicator, indicator_const])
        coefs[indicator] = 1
    model.add_cons_vars(to_add)
    model.solver.update()
    model.objective.set_linear_coefficients(coefs)
    model.objective.direction = "min"