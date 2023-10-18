def build_dag(data, samples):
    """
    build a directed acyclic graph describing jobs to be run in order.
    """

    ## Create DAGs for the assembly method being used, store jobs in nodes
    snames = [i.name for i in samples]
    dag = nx.DiGraph()

    ## get list of pre-align jobs from globals based on assembly method
    joborder = JOBORDER[data.paramsdict["assembly_method"]]

    ## WHICH JOBS TO RUN: iterate over the sample names
    for sname in snames:
        ## append pre-align job for each sample to nodes list
        for func in joborder:
            dag.add_node("{}-{}-{}".format(func, 0, sname))

        ## append align func jobs, each will have max 10
        for chunk in xrange(10):
            dag.add_node("{}-{}-{}".format("muscle_align", chunk, sname))

        ## append final reconcat jobs
        dag.add_node("{}-{}-{}".format("reconcat", 0, sname))

    ## ORDER OF JOBS: add edges/dependency between jobs: (first-this, then-that)
    for sname in snames:
        for sname2 in snames:
            ## enforce that clust/map cannot start until derep is done for ALL
            ## samples. This is b/c...
            dag.add_edge("{}-{}-{}".format(joborder[0], 0, sname2),
                         "{}-{}-{}".format(joborder[1], 0, sname))

        ## add remaining pre-align jobs 
        for idx in xrange(2, len(joborder)):
            dag.add_edge("{}-{}-{}".format(joborder[idx-1], 0, sname),
                         "{}-{}-{}".format(joborder[idx], 0, sname))

        ## Add 10 align jobs, none of which can start until all chunker jobs
        ## are finished. Similarly, reconcat jobs cannot start until all align
        ## jobs are finished.
        for sname2 in snames:
            for chunk in range(10):
                dag.add_edge("{}-{}-{}".format("muscle_chunker", 0, sname2),
                             "{}-{}-{}".format("muscle_align", chunk, sname))
                ## add that the final reconcat job can't start until after
                ## each chunk of its own sample has finished aligning.
                dag.add_edge("{}-{}-{}".format("muscle_align", chunk, sname),
                             "{}-{}-{}".format("reconcat", 0, sname))
    ## return the dag
    return dag, joborder