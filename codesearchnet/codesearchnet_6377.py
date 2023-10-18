def loopless_fva_iter(model, reaction, solution=False, zero_cutoff=None):
    """Plugin to get a loopless FVA solution from single FVA iteration.

    Assumes the following about `model` and `reaction`:
    1. the model objective is set to be `reaction`
    2. the model has been optimized and contains the minimum/maximum flux for
       `reaction`
    3. the model contains an auxiliary variable called "fva_old_objective"
       denoting the previous objective

    Parameters
    ----------
    model : cobra.Model
        The model to be used.
    reaction : cobra.Reaction
        The reaction currently minimized/maximized.
    solution : boolean, optional
        Whether to return the entire solution or only the minimum/maximum for
        `reaction`.
    zero_cutoff : positive float, optional
        Cutoff used for loop removal. Fluxes with an absolute value smaller
        than `zero_cutoff` are considered to be zero (default model.tolerance).

    Returns
    -------
    single float or dict
        Returns the minimized/maximized flux through `reaction` if
        all_fluxes == False (default). Otherwise returns a loopless flux
        solution containing the minimum/maximum flux for `reaction`.
    """
    zero_cutoff = normalize_cutoff(model, zero_cutoff)

    current = model.objective.value
    sol = get_solution(model)
    objective_dir = model.objective.direction

    # boundary reactions can not be part of cycles
    if reaction.boundary:
        if solution:
            return sol
        else:
            return current

    with model:
        _add_cycle_free(model, sol.fluxes)
        model.slim_optimize()

        # If the previous optimum is maintained in the loopless solution it was
        # loopless and we are done
        if abs(reaction.flux - current) < zero_cutoff:
            if solution:
                return sol
            return current

        # If previous optimum was not in the loopless solution create a new
        # almost loopless solution containing only loops including the current
        # reaction. Than remove all of those loops.
        ll_sol = get_solution(model).fluxes
        reaction.bounds = (current, current)
        model.slim_optimize()
        almost_ll_sol = get_solution(model).fluxes

    with model:
        # find the reactions with loops using the current reaction and remove
        # the loops
        for rxn in model.reactions:
            rid = rxn.id
            if ((abs(ll_sol[rid]) < zero_cutoff) and
                    (abs(almost_ll_sol[rid]) > zero_cutoff)):
                rxn.bounds = max(0, rxn.lower_bound), min(0, rxn.upper_bound)

        if solution:
            best = model.optimize()
        else:
            model.slim_optimize()
            best = reaction.flux
    model.objective.direction = objective_dir
    return best