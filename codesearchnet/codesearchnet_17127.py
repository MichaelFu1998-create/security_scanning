def bond_task(
    perc_graph_result, seeds, ps, convolution_factors_tasks_iterator
):
    """
    Perform a number of runs

    The number of runs is the number of seeds

    convolution_factors_tasks_iterator needs to be an iterator

    We shield the convolution factors tasks from jug value/result mechanism
    by supplying an iterator to the list of tasks for lazy evaluation
    http://github.com/luispedro/jug/blob/43f0d80a78f418fd3aa2b8705eaf7c4a5175fff7/jug/task.py#L100
    http://github.com/luispedro/jug/blob/43f0d80a78f418fd3aa2b8705eaf7c4a5175fff7/jug/task.py#L455
    """

    # restore the list of convolution factors tasks
    convolution_factors_tasks = list(convolution_factors_tasks_iterator)

    return reduce(
        percolate.hpc.bond_reduce,
        map(
            bond_run,
            itertools.repeat(perc_graph_result),
            seeds,
            itertools.repeat(ps),
            itertools.repeat(convolution_factors_tasks),
        )
    )