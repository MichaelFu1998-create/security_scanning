def microcanonical_statistics_dtype(spanning_cluster=True):
    """
    Return the numpy structured array data type for sample states

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
    """
    fields = list()
    fields.extend([
        ('n', 'uint32'),
        ('edge', 'uint32'),
    ])
    if spanning_cluster:
        fields.extend([
            ('has_spanning_cluster', 'bool'),
        ])
    fields.extend([
        ('max_cluster_size', 'uint32'),
        ('moments', '(5,)uint64'),
    ])
    return _ndarray_dtype(fields)