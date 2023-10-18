def finalize_canonical_averages(
    number_of_nodes, ps, canonical_averages, alpha,
):
    """
    Finalize canonical averages
    """

    spanning_cluster = (
        (
            'percolation_probability_mean' in
            canonical_averages.dtype.names
        ) and
        'percolation_probability_m2' in canonical_averages.dtype.names
    )

    # append values of p as an additional field
    ret = np.empty_like(
        canonical_averages,
        dtype=finalized_canonical_averages_dtype(
            spanning_cluster=spanning_cluster
        ),
    )

    n = canonical_averages['number_of_runs']
    sqrt_n = np.sqrt(canonical_averages['number_of_runs'])

    ret['number_of_runs'] = n
    ret['p'] = ps
    ret['alpha'] = alpha

    def _transform(
        original_key, final_key=None, normalize=False, transpose=False,
    ):
        if final_key is None:
            final_key = original_key
        keys_mean = [
            '{}_mean'.format(key)
            for key in [original_key, final_key]
        ]
        keys_std = [
            '{}_m2'.format(original_key),
            '{}_std'.format(final_key),
        ]
        key_ci = '{}_ci'.format(final_key)

        # calculate sample mean
        ret[keys_mean[1]] = canonical_averages[keys_mean[0]]
        if normalize:
            ret[keys_mean[1]] /= number_of_nodes

        # calculate sample standard deviation
        array = canonical_averages[keys_std[0]]
        result = np.sqrt(
            (array.T if transpose else array) / (n - 1)
        )
        ret[keys_std[1]] = (
            result.T if transpose else result
        )
        if normalize:
            ret[keys_std[1]] /= number_of_nodes

        # calculate standard normal confidence interval
        array = ret[keys_std[1]]
        scale = (array.T if transpose else array) / sqrt_n
        array = ret[keys_mean[1]]
        mean = (array.T if transpose else array)
        result = scipy.stats.t.interval(
            1 - alpha,
            df=n - 1,
            loc=mean,
            scale=scale,
        )
        (
            ret[key_ci][..., 0], ret[key_ci][..., 1]
        ) = ([my_array.T for my_array in result] if transpose else result)

    if spanning_cluster:
        _transform('percolation_probability')

    _transform('max_cluster_size', 'percolation_strength', normalize=True)
    _transform('moments', normalize=True, transpose=True)

    return ret