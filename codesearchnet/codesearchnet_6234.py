def fix_objective_as_constraint(model, fraction=1, bound=None,
                                name='fixed_objective_{}'):
    """Fix current objective as an additional constraint.

    When adding constraints to a model, such as done in pFBA which
    minimizes total flux, these constraints can become too powerful,
    resulting in solutions that satisfy optimality but sacrifices too
    much for the original objective function. To avoid that, we can fix
    the current objective value as a constraint to ignore solutions that
    give a lower (or higher depending on the optimization direction)
    objective value than the original model.

    When done with the model as a context, the modification to the
    objective will be reverted when exiting that context.

    Parameters
    ----------
    model : cobra.Model
        The model to operate on
    fraction : float
        The fraction of the optimum the objective is allowed to reach.
    bound : float, None
        The bound to use instead of fraction of maximum optimal value. If
        not None, fraction is ignored.
    name : str
        Name of the objective. May contain one `{}` placeholder which is filled
        with the name of the old objective.

    Returns
    -------
        The value of the optimized objective * fraction
    """
    fix_objective_name = name.format(model.objective.name)
    if fix_objective_name in model.constraints:
        model.solver.remove(fix_objective_name)
    if bound is None:
        bound = model.slim_optimize(error_value=None) * fraction
    if model.objective.direction == 'max':
        ub, lb = None, bound
    else:
        ub, lb = bound, None
    constraint = model.problem.Constraint(
        model.objective.expression,
        name=fix_objective_name, ub=ub, lb=lb)
    add_cons_vars_to_problem(model, constraint, sloppy=True)
    return bound