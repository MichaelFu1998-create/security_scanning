def _multi_deletion(model, entity, element_lists, method="fba",
                    solution=None, processes=None, **kwargs):
    """
    Provide a common interface for single or multiple knockouts.

    Parameters
    ----------
    model : cobra.Model
        The metabolic model to perform deletions in.
    entity : 'gene' or 'reaction'
        The entity to knockout (``cobra.Gene`` or ``cobra.Reaction``).
    element_lists : list
        List of iterables ``cobra.Reaction``s or ``cobra.Gene``s (or their IDs)
        to be deleted.
    method: {"fba", "moma", "linear moma", "room", "linear room"}, optional
        Method used to predict the growth rate.
    solution : cobra.Solution, optional
        A previous solution to use as a reference for (linear) MOMA or ROOM.
    processes : int, optional
        The number of parallel processes to run. Can speed up the computations
        if the number of knockouts to perform is large. If not passed,
        will be set to the number of CPUs found.
    kwargs :
        Passed on to underlying simulation functions.

    Returns
    -------
    pandas.DataFrame
        A representation of all combinations of entity deletions. The
        columns are 'growth' and 'status', where

        index : frozenset([str])
            The gene or reaction identifiers that were knocked out.
        growth : float
            The growth rate of the adjusted model.
        status : str
            The solution's status.
    """
    solver = sutil.interface_to_str(model.problem.__name__)
    if method == "moma" and solver not in sutil.qp_solvers:
        raise RuntimeError(
            "Cannot use MOMA since '{}' is not QP-capable."
            "Please choose a different solver or use FBA only.".format(solver))

    if processes is None:
        processes = CONFIGURATION.processes

    with model:
        if "moma" in method:
            add_moma(model, solution=solution, linear="linear" in method)
        elif "room" in method:
            add_room(model, solution=solution, linear="linear" in method,
                     **kwargs)

        args = set([frozenset(comb) for comb in product(*element_lists)])
        processes = min(processes, len(args))

        def extract_knockout_results(result_iter):
            result = pd.DataFrame([
                (frozenset(ids), growth, status)
                for (ids, growth, status) in result_iter
            ], columns=['ids', 'growth', 'status'])
            result.set_index('ids', inplace=True)
            return result

        if processes > 1:
            worker = dict(gene=_gene_deletion_worker,
                          reaction=_reaction_deletion_worker)[entity]
            chunk_size = len(args) // processes
            pool = multiprocessing.Pool(
                processes, initializer=_init_worker, initargs=(model,)
            )
            results = extract_knockout_results(pool.imap_unordered(
                worker,
                args,
                chunksize=chunk_size
            ))
            pool.close()
            pool.join()
        else:
            worker = dict(gene=_gene_deletion,
                          reaction=_reaction_deletion)[entity]
            results = extract_knockout_results(map(
                partial(worker, model), args))
        return results