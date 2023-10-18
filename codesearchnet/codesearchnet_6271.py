def moma(model, solution=None, linear=True):
    """
    Compute a single solution based on (linear) MOMA.

    Compute a new flux distribution that is at a minimal distance to a
    previous reference solution. Minimization of metabolic adjustment (MOMA) is
    generally used to assess the impact
    of knock-outs. Thus the typical usage is to provide a wildtype flux
    distribution as reference and a model in knock-out state.

    Parameters
    ----------
    model : cobra.Model
        The model state to compute a MOMA-based solution for.
    solution : cobra.Solution, optional
        A (wildtype) reference solution.
    linear : bool, optional
        Whether to use the linear MOMA formulation or not (default True).

    Returns
    -------
    cobra.Solution
        A flux distribution that is at a minimal distance compared to the
        reference solution.

    See Also
    --------
    add_moma : add MOMA constraints and objective

    """
    with model:
        add_moma(model=model, solution=solution, linear=linear)
        solution = model.optimize()
    return solution