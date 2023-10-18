def loopless_solution(model, fluxes=None):
    """Convert an existing solution to a loopless one.

    Removes as many loops as possible (see Notes).
    Uses the method from CycleFreeFlux [1]_ and is much faster than
    `add_loopless` and should therefore be the preferred option to get loopless
    flux distributions.

    Parameters
    ----------
    model : cobra.Model
        The model to which to add the constraints.
    fluxes : dict
        A dictionary {rxn_id: flux} that assigns a flux to each reaction. If
        not None will use the provided flux values to obtain a close loopless
        solution.

    Returns
    -------
    cobra.Solution
        A solution object containing the fluxes with the least amount of
        loops possible or None if the optimization failed (usually happening
        if the flux distribution in `fluxes` is infeasible).

    Notes
    -----
    The returned flux solution has the following properties:

    - it contains the minimal number of loops possible and no loops at all if
      all flux bounds include zero
    - it has an objective value close to the original one and the same
      objective value id the objective expression can not form a cycle
      (which is usually true since it consumes metabolites)
    - it has the same exact exchange fluxes as the previous solution
    - all fluxes have the same sign (flow in the same direction) as the
      previous solution

    References
    ----------
    .. [1] CycleFreeFlux: efficient removal of thermodynamically infeasible
       loops from flux distributions. Desouki AA, Jarre F, Gelius-Dietrich
       G, Lercher MJ. Bioinformatics. 2015 Jul 1;31(13):2159-65. doi:
       10.1093/bioinformatics/btv096.
    """
    # Need to reoptimize otherwise spurious solution artifacts can cause
    # all kinds of havoc
    # TODO: check solution status
    if fluxes is None:
        sol = model.optimize(objective_sense=None)
        fluxes = sol.fluxes

    with model:
        prob = model.problem
        # Needs one fixed bound for cplex...
        loopless_obj_constraint = prob.Constraint(
            model.objective.expression,
            lb=-1e32, name="loopless_obj_constraint")
        model.add_cons_vars([loopless_obj_constraint])
        _add_cycle_free(model, fluxes)
        solution = model.optimize(objective_sense=None)
        solution.objective_value = loopless_obj_constraint.primal

    return solution