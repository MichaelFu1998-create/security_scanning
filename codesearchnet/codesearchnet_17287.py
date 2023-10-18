def canonical_averages_dtype(spanning_cluster=True):
    """
    The NumPy Structured Array type for canonical averages over several
    runs

    Helper function

    Parameters
    ----------
    spanning_cluster : bool, optional
        Whether to detect a spanning cluster or not.
        Defaults to ``True``.

    Returns
    -------
    ret : list of pairs of str
        A list of tuples of field names and data types to be used as ``dtype``
        argument in numpy ndarray constructors

    See Also
    --------
    http://docs.scipy.org/doc/numpy/user/basics.rec.html
    canonical_statistics_dtype
    finalized_canonical_averages_dtype
    """
    fields = list()
    fields.extend([
        ('number_of_runs', 'uint32'),
    ])
    if spanning_cluster:
        fields.extend([
            ('percolation_probability_mean', 'float64'),
            ('percolation_probability_m2', 'float64'),
        ])
    fields.extend([
        ('max_cluster_size_mean', 'float64'),
        ('max_cluster_size_m2', 'float64'),
        ('moments_mean', '(5,)float64'),
        ('moments_m2', '(5,)float64'),
    ])
    return _ndarray_dtype(fields)