def add_lp_feasibility(model):
    """
    Add a new objective and variables to ensure a feasible solution.

    The optimized objective will be zero for a feasible solution and otherwise
    represent the distance from feasibility (please see [1]_ for more
    information).

    Parameters
    ----------
    model : cobra.Model
        The model whose feasibility is to be tested.

    References
    ----------
    .. [1] Gomez, Jose A., Kai Höffner, and Paul I. Barton.
    “DFBAlab: A Fast and Reliable MATLAB Code for Dynamic Flux Balance
    Analysis.” BMC Bioinformatics 15, no. 1 (December 18, 2014): 409.
    https://doi.org/10.1186/s12859-014-0409-8.

    """

    obj_vars = []
    prob = model.problem
    for met in model.metabolites:
        s_plus = prob.Variable("s_plus_" + met.id, lb=0)
        s_minus = prob.Variable("s_minus_" + met.id, lb=0)

        model.add_cons_vars([s_plus, s_minus])
        model.constraints[met.id].set_linear_coefficients(
            {s_plus: 1.0, s_minus: -1.0})
        obj_vars.append(s_plus)
        obj_vars.append(s_minus)

    model.objective = prob.Objective(Zero, sloppy=True, direction="min")
    model.objective.set_linear_coefficients({v: 1.0 for v in obj_vars})