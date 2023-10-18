def room(model, solution=None, linear=False, delta=0.03, epsilon=1E-03):
    """
    Compute a single solution based on regulatory on/off minimization (ROOM).

    Compute a new flux distribution that minimizes the number of active
    reactions needed to accommodate a previous reference solution.
    Regulatory on/off minimization (ROOM) is generally used to assess the
    impact of knock-outs. Thus the typical usage is to provide a wildtype flux
    distribution as reference and a model in knock-out state.

    Parameters
    ----------
    model : cobra.Model
        The model state to compute a ROOM-based solution for.
    solution : cobra.Solution, optional
        A (wildtype) reference solution.
    linear : bool, optional
        Whether to use the linear ROOM formulation or not (default False).
    delta: float, optional
        The relative tolerance range (additive) (default 0.03).
    epsilon: float, optional
        The absolute tolerance range (multiplicative) (default 0.001).

    Returns
    -------
    cobra.Solution
        A flux distribution with minimal active reaction changes compared to
        the reference.

    See Also
    --------
    add_room : add ROOM constraints and objective

    """
    with model:
        add_room(model=model, solution=solution, linear=linear, delta=delta,
                 epsilon=epsilon)
        solution = model.optimize()
    return solution