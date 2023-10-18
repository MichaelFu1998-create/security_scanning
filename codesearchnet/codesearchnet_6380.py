def constraint_matrices(model, array_type='dense', include_vars=False,
                        zero_tol=1e-6):
    """Create a matrix representation of the problem.

    This is used for alternative solution approaches that do not use optlang.
    The function will construct the equality matrix, inequality matrix and
    bounds for the complete problem.

    Notes
    -----
    To accomodate non-zero equalities the problem will add the variable
    "const_one" which is a variable that equals one.

    Arguments
    ---------
    model : cobra.Model
        The model from which to obtain the LP problem.
    array_type : string
        The type of array to construct. if 'dense', return a standard
        numpy.array, 'dok', or 'lil' will construct a sparse array using
        scipy of the corresponding type and 'DataFrame' will give a
        pandas `DataFrame` with metabolite indices and reaction columns.
    zero_tol : float
        The zero tolerance used to judge whether two bounds are the same.

    Returns
    -------
    collections.namedtuple
        A named tuple consisting of 6 matrices and 2 vectors:
        - "equalities" is a matrix S such that S*vars = b. It includes a row
          for each constraint and one column for each variable.
        - "b" the right side of the equality equation such that S*vars = b.
        - "inequalities" is a matrix M such that lb <= M*vars <= ub.
          It contains a row for each inequality and as many columns as
          variables.
        - "bounds" is a compound matrix [lb ub] containing the lower and
          upper bounds for the inequality constraints in M.
        - "variable_fixed" is a boolean vector indicating whether the variable
          at that index is fixed (lower bound == upper_bound) and
          is thus bounded by an equality constraint.
        - "variable_bounds" is a compound matrix [lb ub] containing the
          lower and upper bounds for all variables.
    """
    if array_type not in ('DataFrame', 'dense') and not dok_matrix:
        raise ValueError('Sparse matrices require scipy')

    array_builder = {
        'dense': np.array, 'dok': dok_matrix, 'lil': lil_matrix,
        'DataFrame': pd.DataFrame,
    }[array_type]

    Problem = namedtuple("Problem",
                         ["equalities", "b", "inequalities", "bounds",
                          "variable_fixed", "variable_bounds"])
    equality_rows = []
    inequality_rows = []
    inequality_bounds = []
    b = []

    for const in model.constraints:
        lb = -np.inf if const.lb is None else const.lb
        ub = np.inf if const.ub is None else const.ub
        equality = (ub - lb) < zero_tol
        coefs = const.get_linear_coefficients(model.variables)
        coefs = [coefs[v] for v in model.variables]
        if equality:
            b.append(lb if abs(lb) > zero_tol else 0.0)
            equality_rows.append(coefs)
        else:
            inequality_rows.append(coefs)
            inequality_bounds.append([lb, ub])

    var_bounds = np.array([[v.lb, v.ub] for v in model.variables])
    fixed = var_bounds[:, 1] - var_bounds[:, 0] < zero_tol

    results = Problem(
        equalities=array_builder(equality_rows),
        b=np.array(b),
        inequalities=array_builder(inequality_rows),
        bounds=array_builder(inequality_bounds),
        variable_fixed=np.array(fixed),
        variable_bounds=array_builder(var_bounds))

    return results