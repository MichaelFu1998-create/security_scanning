def random_2in4sat(num_variables, num_clauses, vartype=dimod.BINARY, satisfiable=True):
    """Random two-in-four (2-in-4) constraint satisfaction problem.

    Args:
        num_variables (integer): Number of variables (at least four).
        num_clauses (integer): Number of constraints that together constitute the
            constraint satisfaction problem.
        vartype (Vartype, optional, default='BINARY'): Variable type. Accepted
            input values:

            * Vartype.SPIN, 'SPIN', {-1, 1}
            * Vartype.BINARY, 'BINARY', {0, 1}
        satisfiable (bool, optional, default=True): True if the CSP can be satisfied.

    Returns:
        CSP (:obj:`.ConstraintSatisfactionProblem`): CSP that is satisfied when its variables
        are assigned values that satisfy a two-in-four satisfiability problem.

    Examples:
        This example creates a CSP with 6 variables and two random constraints and checks
        whether a particular assignment of variables satisifies it.

        >>> import dwavebinarycsp
        >>> import dwavebinarycsp.factories as sat
        >>> csp = sat.random_2in4sat(6, 2)
        >>> csp.constraints    # doctest: +SKIP
        [Constraint.from_configurations(frozenset({(1, 0, 1, 0), (1, 0, 0, 1), (1, 1, 1, 1), (0, 1, 1, 0), (0, 0, 0, 0),
         (0, 1, 0, 1)}), (2, 4, 0, 1), Vartype.BINARY, name='2-in-4'),
         Constraint.from_configurations(frozenset({(1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0), (0, 0, 0, 1),
         (0, 1, 0, 0), (0, 0, 1, 0)}), (1, 2, 4, 5), Vartype.BINARY, name='2-in-4')]
        >>> csp.check({0: 1, 1: 0, 2: 1, 3: 1, 4: 0, 5: 0})       # doctest: +SKIP
        True


    """

    if num_variables < 4:
        raise ValueError("a 2in4 problem needs at least 4 variables")
    if num_clauses > 16 * _nchoosek(num_variables, 4):  # 16 different negation patterns
        raise ValueError("too many clauses")

    # also checks the vartype argument
    csp = ConstraintSatisfactionProblem(vartype)

    variables = list(range(num_variables))

    constraints = set()

    if satisfiable:
        values = tuple(vartype.value)
        planted_solution = {v: choice(values) for v in variables}

        configurations = [(0, 0, 1, 1), (0, 1, 0, 1), (1, 0, 0, 1),
                          (0, 1, 1, 0), (1, 0, 1, 0), (1, 1, 0, 0)]

        while len(constraints) < num_clauses:
            # sort the variables because constraints are hashed on configurations/variables
            # because 2-in-4 sat is symmetric, we would not get a hash conflict for different
            # variable orders
            constraint_variables = sorted(sample(variables, 4))

            # pick (uniformly) a configuration and determine which variables we need to negate to
            # match the chosen configuration
            config = choice(configurations)
            pos = tuple(v for idx, v in enumerate(constraint_variables) if config[idx] == (planted_solution[v] > 0))
            neg = tuple(v for idx, v in enumerate(constraint_variables) if config[idx] != (planted_solution[v] > 0))

            const = sat2in4(pos=pos, neg=neg, vartype=vartype)

            assert const.check(planted_solution)

            constraints.add(const)
    else:
        while len(constraints) < num_clauses:
            # sort the variables because constraints are hashed on configurations/variables
            # because 2-in-4 sat is symmetric, we would not get a hash conflict for different
            # variable orders
            constraint_variables = sorted(sample(variables, 4))

            # randomly determine negations
            pos = tuple(v for v in constraint_variables if random() > .5)
            neg = tuple(v for v in constraint_variables if v not in pos)

            const = sat2in4(pos=pos, neg=neg, vartype=vartype)

            constraints.add(const)

    for const in constraints:
        csp.add_constraint(const)

    # in case any variables didn't make it in
    for v in variables:
        csp.add_variable(v)

    return csp