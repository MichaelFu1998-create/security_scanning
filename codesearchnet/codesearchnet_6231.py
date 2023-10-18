def add_cons_vars_to_problem(model, what, **kwargs):
    """Add variables and constraints to a Model's solver object.

    Useful for variables and constraints that can not be expressed with
    reactions and lower/upper bounds. Will integrate with the Model's context
    manager in order to revert changes upon leaving the context.

    Parameters
    ----------
    model : a cobra model
       The model to which to add the variables and constraints.
    what : list or tuple of optlang variables or constraints.
       The variables or constraints to add to the model. Must be of class
       `model.problem.Variable` or
       `model.problem.Constraint`.
    **kwargs : keyword arguments
        passed to solver.add()
    """
    context = get_context(model)

    model.solver.add(what, **kwargs)
    if context:
        context(partial(model.solver.remove, what))