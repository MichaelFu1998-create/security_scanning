def find_blocked_reactions(model,
                           reaction_list=None,
                           zero_cutoff=None,
                           open_exchanges=False,
                           processes=None):
    """
    Find reactions that cannot carry any flux.

    The question whether or not a reaction is blocked is highly dependent
    on the current exchange reaction settings for a COBRA model. Hence an
    argument is provided to open all exchange reactions.

    Notes
    -----
    Sink and demand reactions are left untouched. Please modify them manually.

    Parameters
    ----------
    model : cobra.Model
        The model to analyze.
    reaction_list : list, optional
        List of reactions to consider, the default includes all model
        reactions.
    zero_cutoff : float, optional
        Flux value which is considered to effectively be zero
        (default model.tolerance).
    open_exchanges : bool, optional
        Whether or not to open all exchange reactions to very high flux ranges.
    processes : int, optional
        The number of parallel processes to run. Can speed up the computations
        if the number of reactions is large. If not explicitly
        passed, it will be set from the global configuration singleton.

    Returns
    -------
    list
        List with the identifiers of blocked reactions.

    """
    zero_cutoff = normalize_cutoff(model, zero_cutoff)

    with model:
        if open_exchanges:
            for reaction in model.exchanges:
                reaction.bounds = (min(reaction.lower_bound, -1000),
                                   max(reaction.upper_bound, 1000))
        if reaction_list is None:
            reaction_list = model.reactions
        # Limit the search space to reactions which have zero flux. If the
        # reactions already carry flux in this solution,
        # then they cannot be blocked.
        model.slim_optimize()
        solution = get_solution(model, reactions=reaction_list)
        reaction_list = solution.fluxes[
            solution.fluxes.abs() < zero_cutoff].index.tolist()
        # Run FVA to find reactions where both the minimal and maximal flux
        # are zero (below the cut off).
        flux_span = flux_variability_analysis(
            model, fraction_of_optimum=0., reaction_list=reaction_list,
            processes=processes
        )
        return flux_span[
            flux_span.abs().max(axis=1) < zero_cutoff].index.tolist()