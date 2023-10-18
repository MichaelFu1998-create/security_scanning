def add_linear_obj(model):
    """Add a linear version of a minimal medium to the model solver.

    Changes the optimization objective to finding the growth medium requiring
    the smallest total import flux::

        minimize sum |r_i| for r_i in import_reactions

    Arguments
    ---------
    model : cobra.Model
        The model to modify.
    """
    coefs = {}
    for rxn in find_boundary_types(model, "exchange"):
        export = len(rxn.reactants) == 1
        if export:
            coefs[rxn.reverse_variable] = 1
        else:
            coefs[rxn.forward_variable] = 1
    model.objective.set_linear_coefficients(coefs)
    model.objective.direction = "min"