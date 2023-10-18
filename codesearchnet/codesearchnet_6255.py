def gapfill(model, universal=None, lower_bound=0.05,
            penalties=None, demand_reactions=True, exchange_reactions=False,
            iterations=1):
    """Perform gapfilling on a model.

    See documentation for the class GapFiller.

    Parameters
    ----------
    model : cobra.Model
        The model to perform gap filling on.
    universal : cobra.Model, None
        A universal model with reactions that can be used to complete the
        model. Only gapfill considering demand and exchange reactions if
        left missing.
    lower_bound : float
        The minimally accepted flux for the objective in the filled model.
    penalties : dict, None
        A dictionary with keys being 'universal' (all reactions included in
        the universal model), 'exchange' and 'demand' (all additionally
        added exchange and demand reactions) for the three reaction types.
        Can also have reaction identifiers for reaction specific costs.
        Defaults are 1, 100 and 1 respectively.
    iterations : int
        The number of rounds of gapfilling to perform. For every iteration,
        the penalty for every used reaction increases linearly. This way,
        the algorithm is encouraged to search for alternative solutions
        which may include previously used reactions. I.e., with enough
        iterations pathways including 10 steps will eventually be reported
        even if the shortest pathway is a single reaction.
    exchange_reactions : bool
        Consider adding exchange (uptake) reactions for all metabolites
        in the model.
    demand_reactions : bool
        Consider adding demand reactions for all metabolites.

    Returns
    -------
    iterable
        list of lists with on set of reactions that completes the model per
        requested iteration.

    Examples
    --------
    >>> import cobra.test as ct
    >>> from cobra import Model
    >>> from cobra.flux_analysis import gapfill
    >>> model = ct.create_test_model("salmonella")
    >>> universal = Model('universal')
    >>> universal.add_reactions(model.reactions.GF6PTA.copy())
    >>> model.remove_reactions([model.reactions.GF6PTA])
    >>> gapfill(model, universal)
    """
    gapfiller = GapFiller(model, universal=universal,
                          lower_bound=lower_bound, penalties=penalties,
                          demand_reactions=demand_reactions,
                          exchange_reactions=exchange_reactions)
    return gapfiller.fill(iterations=iterations)