def find_essential_genes(model, threshold=None, processes=None):
    """
    Return a set of essential genes.

    A gene is considered essential if restricting the flux of all reactions
    that depend on it to zero causes the objective, e.g., the growth rate,
    to also be zero, below the threshold, or infeasible.

    Parameters
    ----------
    model : cobra.Model
        The model to find the essential genes for.
    threshold : float, optional
        Minimal objective flux to be considered viable. By default this is
        1% of the maximal objective.
    processes : int, optional
        The number of parallel processes to run. If not passed,
        will be set to the number of CPUs found.
    processes : int, optional
        The number of parallel processes to run. Can speed up the computations
        if the number of knockouts to perform is large. If not explicitly
        passed, it will be set from the global configuration singleton.

    Returns
    -------
    set
        Set of essential genes
    """
    if threshold is None:
        threshold = model.slim_optimize(error_value=None) * 1E-02
    deletions = single_gene_deletion(model, method='fba', processes=processes)
    essential = deletions.loc[deletions['growth'].isna() |
                              (deletions['growth'] < threshold), :].index
    return {model.genes.get_by_id(g) for ids in essential for g in ids}