def remove_cons_vars_from_problem(model, what):
    """Remove variables and constraints from a Model's solver object.

    Useful to temporarily remove variables and constraints from a Models's
    solver object.

    Parameters
    ----------
    model : a cobra model
       The model from which to remove the variables and constraints.
    what : list or tuple of optlang variables or constraints.
       The variables or constraints to remove from the model. Must be of
       class `model.problem.Variable` or
       `model.problem.Constraint`.
    """
    context = get_context(model)

    model.solver.remove(what)
    if context:
        context(partial(model.solver.add, what))