def set_objective(model, value, additive=False):
    """Set the model objective.

    Parameters
    ----------
    model : cobra model
       The model to set the objective for
    value : model.problem.Objective,
            e.g. optlang.glpk_interface.Objective, sympy.Basic or dict

        If the model objective is linear, the value can be a new Objective
        object or a dictionary with linear coefficients where each key is a
        reaction and the element the new coefficient (float).

        If the objective is not linear and `additive` is true, only values
        of class Objective.

    additive : boolmodel.reactions.Biomass_Ecoli_core.bounds = (0.1, 0.1)
        If true, add the terms to the current objective, otherwise start with
        an empty objective.
    """
    interface = model.problem
    reverse_value = model.solver.objective.expression
    reverse_value = interface.Objective(
        reverse_value, direction=model.solver.objective.direction,
        sloppy=True)

    if isinstance(value, dict):
        if not model.objective.is_Linear:
            raise ValueError('can only update non-linear objectives '
                             'additively using object of class '
                             'model.problem.Objective, not %s' %
                             type(value))

        if not additive:
            model.solver.objective = interface.Objective(
                Zero, direction=model.solver.objective.direction)
        for reaction, coef in value.items():
            model.solver.objective.set_linear_coefficients(
                {reaction.forward_variable: coef,
                 reaction.reverse_variable: -coef})

    elif isinstance(value, (Basic, optlang.interface.Objective)):
        if isinstance(value, Basic):
            value = interface.Objective(
                value, direction=model.solver.objective.direction,
                sloppy=False)
        # Check whether expression only uses variables from current model
        # clone the objective if not, faster than cloning without checking
        if not _valid_atoms(model, value.expression):
            value = interface.Objective.clone(value, model=model.solver)

        if not additive:
            model.solver.objective = value
        else:
            model.solver.objective += value.expression
    else:
        raise TypeError(
            '%r is not a valid objective for %r.' % (value, model.solver))

    context = get_context(model)
    if context:
        def reset():
            model.solver.objective = reverse_value
            model.solver.objective.direction = reverse_value.direction

        context(reset)