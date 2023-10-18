def get_solver_name(mip=False, qp=False):
    """Select a solver for a given optimization problem.

    Parameters
    ----------
    mip : bool
        Does the solver require mixed integer linear programming capabilities?
    qp : bool
        Does the solver require quadratic programming capabilities?

    Returns
    -------
    string
        The name of feasible solver.

    Raises
    ------
    SolverNotFound
        If no suitable solver could be found.
    """
    if len(solvers) == 0:
        raise SolverNotFound("no solvers installed")
    # Those lists need to be updated as optlang implements more solvers
    mip_order = ["gurobi", "cplex", "glpk"]
    lp_order = ["glpk", "cplex", "gurobi"]
    qp_order = ["gurobi", "cplex"]

    if mip is False and qp is False:
        for solver_name in lp_order:
            if solver_name in solvers:
                return solver_name
        # none of them are in the list order - so return the first one
        return list(solvers)[0]
    elif qp:  # mip does not yet matter for this determination
        for solver_name in qp_order:
            if solver_name in solvers:
                return solver_name
        raise SolverNotFound("no qp-capable solver found")
    else:
        for solver_name in mip_order:
            if solver_name in solvers:
                return solver_name
    raise SolverNotFound("no mip-capable solver found")