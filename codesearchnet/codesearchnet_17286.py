def bond_canonical_statistics(
    microcanonical_statistics,
    convolution_factors,
    **kwargs
):
    """
    canonical cluster statistics for a single run and a single probability

    Parameters
    ----------

    microcanonical_statistics : ndarray
        Return value of `bond_microcanonical_statistics`

    convolution_factors : 1-D array_like
        The coefficients of the convolution for the given probabilty ``p``
        and for each occupation number ``n``.

    Returns
    -------
    ret : ndarray of size ``1``
        Structured array with dtype as returned by
        `canonical_statistics_dtype`

    ret['percolation_probability'] : ndarray of float
        The "percolation probability" of this run at the value of ``p``.
        Only exists if `microcanonical_statistics` argument has the
        ``has_spanning_cluster`` field.

    ret['max_cluster_size'] : ndarray of int
        Weighted size of the largest cluster (absolute number of sites)

    ret['moments'] : 1-D :py:class:`numpy.ndarray` of float
        Array of size ``5``.
        The ``k``-th entry is the weighted ``k``-th raw moment of the
        (absolute) cluster size distribution, with ``k`` ranging from ``0`` to
        ``4``.

    See Also
    --------

    bond_microcanonical_statistics
    canonical_statistics_dtype

    """
    # initialize return array
    spanning_cluster = (
        'has_spanning_cluster' in microcanonical_statistics.dtype.names
    )
    ret = np.empty(1, dtype=canonical_statistics_dtype(spanning_cluster))

    # compute percolation probability
    if spanning_cluster:
        ret['percolation_probability'] = np.sum(
            convolution_factors *
            microcanonical_statistics['has_spanning_cluster']
        )

    # convolve maximum cluster size
    ret['max_cluster_size'] = np.sum(
        convolution_factors *
        microcanonical_statistics['max_cluster_size']
    )

    # convolve moments
    ret['moments'] = np.sum(
        convolution_factors[:, np.newaxis] *
        microcanonical_statistics['moments'],
        axis=0,
    )

    # return convolved cluster statistics
    return ret