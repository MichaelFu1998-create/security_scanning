def canonical_statistics_dtype(spanning_cluster=True):
    """
    The NumPy Structured Array type for canonical statistics

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
    microcanoncial_statistics_dtype
    canonical_averages_dtype
    """
    fields = list()
    if spanning_cluster:
        fields.extend([
            ('percolation_probability', 'float64'),
        ])
    fields.extend([
        ('max_cluster_size', 'float64'),
        ('moments', '(5,)float64'),
    ])
    return _ndarray_dtype(fields)