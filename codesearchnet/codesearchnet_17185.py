def statistics(
    graph, ps, spanning_cluster=True, model='bond', alpha=alpha_1sigma, runs=40
):
    """
    Helper function to compute percolation statistics

    See Also
    --------

    canonical_averages

    microcanonical_averages

    sample_states

    """

    my_microcanonical_averages = microcanonical_averages(
        graph=graph, runs=runs, spanning_cluster=spanning_cluster, model=model,
        alpha=alpha
    )

    my_microcanonical_averages_arrays = microcanonical_averages_arrays(
        my_microcanonical_averages
    )

    return canonical_averages(ps, my_microcanonical_averages_arrays)