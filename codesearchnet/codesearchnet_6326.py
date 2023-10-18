def single_reaction_deletion(model, reaction_list=None, method="fba",
                             solution=None, processes=None, **kwargs):
    """
    Knock out each reaction from a given list.

    Parameters
    ----------
    model : cobra.Model
        The metabolic model to perform deletions in.
    reaction_list : iterable, optional
        ``cobra.Reaction``s to be deleted. If not passed,
        all the reactions from the model are used.
    method: {"fba", "moma", "linear moma", "room", "linear room"}, optional
        Method used to predict the growth rate.
    solution : cobra.Solution, optional
        A previous solution to use as a reference for (linear) MOMA or ROOM.
    processes : int, optional
        The number of parallel processes to run. Can speed up the computations
        if the number of knockouts to perform is large. If not passed,
        will be set to the number of CPUs found.
    kwargs :
        Keyword arguments are passed on to underlying simulation functions
        such as ``add_room``.

    Returns
    -------
    pandas.DataFrame
        A representation of all single reaction deletions. The columns are
        'growth' and 'status', where

        index : frozenset([str])
            The reaction identifier that was knocked out.
        growth : float
            The growth rate of the adjusted model.
        status : str
            The solution's status.

    """
    return _multi_deletion(
        model, 'reaction',
        element_lists=_element_lists(model.reactions, reaction_list),
        method=method, solution=solution, processes=processes, **kwargs)