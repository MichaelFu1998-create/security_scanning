def parallel_graph_evaluation(data, adj_matrix, nb_runs=16,
                              nb_jobs=None, **kwargs):
    """Parallelize the various runs of CGNN to evaluate a graph."""
    nb_jobs = SETTINGS.get_default(nb_jobs=nb_jobs)
    if nb_runs == 1:
        return graph_evaluation(data, adj_matrix, **kwargs)
    else:
        output = Parallel(n_jobs=nb_jobs)(delayed(graph_evaluation)(data, adj_matrix,
                                          idx=run, gpu_id=run % SETTINGS.GPU,
                                          **kwargs) for run in range(nb_runs))
        return np.mean(output)