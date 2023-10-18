def bond_initialize_canonical_averages(
    canonical_statistics, **kwargs
):
    """
    Initialize the canonical averages from a single-run cluster statistics

    Parameters
    ----------
    canonical_statistics : 1-D structured ndarray
        Typically contains the canonical statistics for a range of values
        of the occupation probability ``p``.
        The dtype is the result of `canonical_statistics_dtype`.

    Returns
    -------
    ret : structured ndarray
        The dype is the result of `canonical_averages_dtype`.

    ret['number_of_runs'] : 1-D ndarray of int
        Equals ``1`` (initial run).

    ret['percolation_probability_mean'] : 1-D array of float
        Equals ``canonical_statistics['percolation_probability']``
        (if ``percolation_probability`` is present)

    ret['percolation_probability_m2'] : 1-D array of float
        Each entry is ``0.0``

    ret['max_cluster_size_mean'] : 1-D array of float
        Equals ``canonical_statistics['max_cluster_size']``

    ret['max_cluster_size_m2'] : 1-D array of float
        Each entry is ``0.0``

    ret['moments_mean'] : 2-D array of float
        Equals ``canonical_statistics['moments']``

    ret['moments_m2'] : 2-D array of float
        Each entry is ``0.0``

    See Also
    --------
    canonical_averages_dtype
    bond_canonical_statistics

    """
    # initialize return array
    spanning_cluster = (
        'percolation_probability' in canonical_statistics.dtype.names
    )
    # array should have the same size as the input array
    ret = np.empty_like(
        canonical_statistics,
        dtype=canonical_averages_dtype(spanning_cluster=spanning_cluster),
    )
    ret['number_of_runs'] = 1

    # initialize percolation probability mean and sum of squared differences
    if spanning_cluster:
        ret['percolation_probability_mean'] = (
            canonical_statistics['percolation_probability']
        )
        ret['percolation_probability_m2'] = 0.0

    # initialize maximum cluster size mean and sum of squared differences
    ret['max_cluster_size_mean'] = (
        canonical_statistics['max_cluster_size']
    )
    ret['max_cluster_size_m2'] = 0.0

    # initialize moments means and sums of squared differences
    ret['moments_mean'] = canonical_statistics['moments']
    ret['moments_m2'] = 0.0

    return ret