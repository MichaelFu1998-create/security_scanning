def double_reaction_deletion(model, reaction_list1=None, reaction_list2=None,
                             method="fba", solution=None, processes=None,
                             **kwargs):
    """
    Knock out each reaction pair from the combinations of two given lists.

    We say 'pair' here but the order order does not matter.

    Parameters
    ----------
    model : cobra.Model
        The metabolic model to perform deletions in.
    reaction_list1 : iterable, optional
        First iterable of ``cobra.Reaction``s to be deleted. If not passed,
        all the reactions from the model are used.
    reaction_list2 : iterable, optional
        Second iterable of ``cobra.Reaction``s to be deleted. If not passed,
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
        A representation of all combinations of reaction deletions. The
        columns are 'growth' and 'status', where

        index : frozenset([str])
            The reaction identifiers that were knocked out.
        growth : float
            The growth rate of the adjusted model.
        status : str
            The solution's status.

    """

    reaction_list1, reaction_list2 = _element_lists(model.reactions,
                                                    reaction_list1,
                                                    reaction_list2)
    return _multi_deletion(
        model, 'reaction', element_lists=[reaction_list1, reaction_list2],
        method=method, solution=solution, processes=processes, **kwargs)