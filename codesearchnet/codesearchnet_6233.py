def add_absolute_expression(model, expression, name="abs_var", ub=None,
                            difference=0, add=True):
    """Add the absolute value of an expression to the model.

    Also defines a variable for the absolute value that can be used in other
    objectives or constraints.

    Parameters
    ----------
    model : a cobra model
       The model to which to add the absolute expression.
    expression : A sympy expression
       Must be a valid expression within the Model's solver object. The
       absolute value is applied automatically on the expression.
    name : string
       The name of the newly created variable.
    ub : positive float
       The upper bound for the variable.
    difference : positive float
        The difference between the expression and the variable.
    add : bool
        Whether to add the variable to the model at once.

    Returns
    -------
    namedtuple
        A named tuple with variable and two constraints (upper_constraint,
        lower_constraint) describing the new variable and the constraints
        that assign the absolute value of the expression to it.
    """
    Components = namedtuple('Components', ['variable', 'upper_constraint',
                                           'lower_constraint'])
    variable = model.problem.Variable(name, lb=0, ub=ub)
    # The following constraints enforce variable > expression and
    # variable > -expression
    upper_constraint = model.problem.Constraint(expression - variable,
                                                ub=difference,
                                                name="abs_pos_" + name),
    lower_constraint = model.problem.Constraint(expression + variable,
                                                lb=difference,
                                                name="abs_neg_" + name)
    to_add = Components(variable, upper_constraint, lower_constraint)
    if add:
        add_cons_vars_to_problem(model, to_add)
    return to_add