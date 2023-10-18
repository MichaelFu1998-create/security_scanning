def choose_solver(model, solver=None, qp=False):
    """Choose a solver given a solver name and model.

    This will choose a solver compatible with the model and required
    capabilities. Also respects model.solver where it can.

    Parameters
    ----------
    model : a cobra model
        The model for which to choose the solver.
    solver : str, optional
        The name of the solver to be used.
    qp : boolean, optional
        Whether the solver needs Quadratic Programming capabilities.

    Returns
    -------
    solver : an optlang solver interface
        Returns a valid solver for the problem.

    Raises
    ------
    SolverNotFound
        If no suitable solver could be found.
    """
    if solver is None:
        solver = model.problem
    else:
        model.solver = solver

    # Check for QP, raise error if no QP solver found
    if qp and interface_to_str(solver) not in qp_solvers:
        solver = solvers[get_solver_name(qp=True)]

    return solver