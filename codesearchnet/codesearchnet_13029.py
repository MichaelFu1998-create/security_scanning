def new_apply_jobs(data, samples, ipyclient, nthreads, maxindels, force):
    """
    Create a DAG of prealign jobs to be run in order for each sample. Track
    Progress, report errors. Each assembly method has a slightly different
    DAG setup, calling different functions.
    """

    ## is datatype gbs? used in alignment-trimming by align_and_parse()
    is_gbs = bool("gbs" in data.paramsdict["datatype"])

    ## Two view objects, threaded and unthreaded
    lbview = ipyclient.load_balanced_view()
    start = time.time()
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    firstfunc = "derep_concat_split"
    printstr = " {}    | {} | s3 |".format(PRINTSTR[firstfunc], elapsed)
    #printstr = " {}      | {} | s3 |".format(PRINTSTR[], elapsed)
    progressbar(10, 0, printstr, spacer=data._spacer)

    ## TODO: for HPC systems this should be done to make sure targets are spread
    ## among different nodes.
    if nthreads:
        if nthreads < len(ipyclient.ids):
            thview = ipyclient.load_balanced_view(targets=ipyclient.ids[::nthreads])
        elif nthreads == 1:
            thview = ipyclient.load_balanced_view()
        else:
            if len(ipyclient) > 40:
                thview = ipyclient.load_balanced_view(targets=ipyclient.ids[::4])
            else:
                thview = ipyclient.load_balanced_view(targets=ipyclient.ids[::2])


    ## get list of jobs/dependencies as a DAG for all pre-align funcs.
    dag, joborder = build_dag(data, samples)

    ## dicts for storing submitted jobs and results
    results = {}

    ## submit jobs to the engines in single or threaded views. The topological
    ## sort makes sure jobs are input with all dependencies found.
    for node in nx.topological_sort(dag):
        ## get list of async results leading to this job
        deps = [results.get(n) for n in dag.predecessors(node)]
        deps = ipp.Dependency(dependencies=deps, failure=True)

        ## get func, sample, and args for this func (including [data, sample])
        funcstr, chunk, sname = node.split("-", 2)
        func = FUNCDICT[funcstr]
        sample = data.samples[sname]

        ## args vary depending on the function
        if funcstr in ["derep_concat_split", "cluster"]:
            args = [data, sample, nthreads, force]
        elif funcstr in ["mapreads"]:
            args = [data, sample, nthreads, force]
        elif funcstr in ["build_clusters"]:
            args = [data, sample, maxindels]
        elif funcstr in ["muscle_align"]:
            handle = os.path.join(data.tmpdir, 
                        "{}_chunk_{}.ali".format(sample.name, chunk))
            args = [handle, maxindels, is_gbs]
        else:
            args = [data, sample]

        # submit and store AsyncResult object. Some jobs are threaded.
        if nthreads and (funcstr in THREADED_FUNCS):
            #LOGGER.info('submitting %s to %s-threaded view', funcstr, nthreads)
            with thview.temp_flags(after=deps, block=False):
                results[node] = thview.apply(func, *args)
        else:
            #LOGGER.info('submitting %s to single-threaded view', funcstr)
            with lbview.temp_flags(after=deps, block=False):
                results[node] = lbview.apply(func, *args)

    ## track jobs as they finish, abort if someone fails. This blocks here
    ## until all jobs are done. Keep track of which samples have failed so
    ## we only print the first error message.
    sfailed = set()
    for funcstr in joborder + ["muscle_align", "reconcat"]:
        errfunc, sfails, msgs = trackjobs(funcstr, results, spacer=data._spacer)
        LOGGER.info("{}-{}-{}".format(errfunc, sfails, msgs))
        if errfunc:
            for sidx in xrange(len(sfails)):
                sname = sfails[sidx]
                errmsg = msgs[sidx]
                if sname not in sfailed:
                    print("  sample [{}] failed. See error in ./ipyrad_log.txt"\
                          .format(sname))
                    LOGGER.error("sample [%s] failed in step [%s]; error: %s",
                                  sname, errfunc, errmsg)
                    sfailed.add(sname)

    ## Cleanup of successful samples, skip over failed samples
    badaligns = {}
    for sample in samples:
        ## The muscle_align step returns the number of excluded bad alignments
        for async in results:
            func, chunk, sname = async.split("-", 2)
            if (func == "muscle_align") and (sname == sample.name):
                if results[async].successful():
                    badaligns[sample] = int(results[async].get())

    ## for the samples that were successful:
    for sample in badaligns:
        ## store the result
        sample.stats_dfs.s3.filtered_bad_align = badaligns[sample]
        ## store all results
        try:
            sample_cleanup(data, sample)
        except Exception as inst:
            msg = "  Sample {} failed this step. See ipyrad_log.txt.\
                  ".format(sample.name)
            print(msg)
            LOGGER.error("%s - %s", sample.name, inst)

    ## store the results to data
    data_cleanup(data)