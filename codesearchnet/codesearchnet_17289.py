def bond_reduce(row_a, row_b):
    """
    Reduce the canonical averages over several runs

    This is a "true" reducer.
    It is associative and commutative.

    This is a wrapper around `simoa.stats.online_variance`.

    Parameters
    ----------
    row_a, row_b : structured ndarrays
        Output of this function, or initial input from
        `bond_initialize_canonical_averages`

    Returns
    -------
    ret : structured ndarray
        Array is of dtype as returned by `canonical_averages_dtype`

    See Also
    --------
    bond_initialize_canonical_averages
    canonical_averages_dtype
    simoa.stats.online_variance
    """
    spanning_cluster = (
        'percolation_probability_mean' in row_a.dtype.names and
        'percolation_probability_mean' in row_b.dtype.names and
        'percolation_probability_m2' in row_a.dtype.names and
        'percolation_probability_m2' in row_b.dtype.names
    )

    # initialize return array
    ret = np.empty_like(row_a)

    def _reducer(key, transpose=False):
        mean_key = '{}_mean'.format(key)
        m2_key = '{}_m2'.format(key)
        res = simoa.stats.online_variance(*[
            (
                row['number_of_runs'],
                row[mean_key].T if transpose else row[mean_key],
                row[m2_key].T if transpose else row[m2_key],
            )
            for row in [row_a, row_b]
        ])

        (
            ret[mean_key],
            ret[m2_key],
        ) = (
            res[1].T,
            res[2].T,
        ) if transpose else res[1:]

    if spanning_cluster:
        _reducer('percolation_probability')

    _reducer('max_cluster_size')
    _reducer('moments', transpose=True)

    ret['number_of_runs'] = row_a['number_of_runs'] + row_b['number_of_runs']

    return ret