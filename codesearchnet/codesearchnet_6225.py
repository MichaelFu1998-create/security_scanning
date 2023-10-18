def linear_reaction_coefficients(model, reactions=None):
    """Coefficient for the reactions in a linear objective.

    Parameters
    ----------
    model : cobra model
        the model object that defined the objective
    reactions : list
        an optional list for the reactions to get the coefficients for. All
        reactions if left missing.

    Returns
    -------
    dict
        A dictionary where the key is the reaction object and the value is
        the corresponding coefficient. Empty dictionary if there are no
        linear terms in the objective.
    """
    linear_coefficients = {}
    reactions = model.reactions if not reactions else reactions
    try:
        objective_expression = model.solver.objective.expression
        coefficients = objective_expression.as_coefficients_dict()
    except AttributeError:
        return linear_coefficients
    for rxn in reactions:
        forward_coefficient = coefficients.get(rxn.forward_variable, 0)
        reverse_coefficient = coefficients.get(rxn.reverse_variable, 0)
        if forward_coefficient != 0:
            if forward_coefficient == -reverse_coefficient:
                linear_coefficients[rxn] = float(forward_coefficient)
    return linear_coefficients