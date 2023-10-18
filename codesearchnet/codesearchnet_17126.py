def bond_run(perc_graph_result, seed, ps, convolution_factors_tasks):
    """
    Perform a single run (realization) over all microstates and return the
    canonical cluster statistics
    """
    microcanonical_statistics = percolate.hpc.bond_microcanonical_statistics(
        seed=seed, **perc_graph_result
    )

    # initialize statistics array
    canonical_statistics = np.empty(
        ps.size,
        dtype=percolate.hpc.canonical_statistics_dtype(
            spanning_cluster=SPANNING_CLUSTER,
        )
    )

    # loop over all p's and convolve canonical statistics
    # http://docs.scipy.org/doc/numpy/reference/arrays.nditer.html#modifying-array-values
    for row, convolution_factors_task in zip(
        np.nditer(canonical_statistics, op_flags=['writeonly']),
        convolution_factors_tasks,
    ):
        # load task result
        # http://jug.readthedocs.org/en/latest/api.html#jug.Task.load
        assert not convolution_factors_task.is_loaded()
        convolution_factors_task.load()
        # fetch task result
        my_convolution_factors = convolution_factors_task.result

        # convolve to canonical statistics
        row[...] = percolate.hpc.bond_canonical_statistics(
            microcanonical_statistics=microcanonical_statistics,
            convolution_factors=my_convolution_factors,
            spanning_cluster=SPANNING_CLUSTER,
        )
        # explicitly unload task to save memory
        # http://jug.readthedocs.org/en/latest/api.html#jug.Task.unload
        convolution_factors_task.unload()

    # initialize canonical averages for reduce
    ret = percolate.hpc.bond_initialize_canonical_averages(
        canonical_statistics=canonical_statistics,
        spanning_cluster=SPANNING_CLUSTER,
    )

    return ret