def multi_muscle_align(data, samples, ipyclient):
    """
    Sends the cluster bits to nprocessors for muscle alignment. They return
    with indel.h5 handles to be concatenated into a joint h5.
    """
    LOGGER.info("starting alignments")

    ## get client
    lbview = ipyclient.load_balanced_view()
    start = time.time()
    printstr = " aligning clusters     | {} | s6 |"
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(20, 0, printstr.format(elapsed), spacer=data._spacer)

    ## submit clustbits as jobs to engines. The chunkfiles are removed when they
    ## are finished so this job can even be restarted if it was half finished, 
    ## though that is probably rare. 
    path = os.path.join(data.tmpdir, data.name + ".chunk_*")
    clustbits = glob.glob(path)
    jobs = {}
    for idx in xrange(len(clustbits)):
        args = [data, samples, clustbits[idx]]
        jobs[idx] = lbview.apply(persistent_popen_align3, *args)
    allwait = len(jobs)
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(20, 0, printstr.format(elapsed), spacer=data._spacer)

    ## print progress while bits are aligning
    while 1:
        finished = [i.ready() for i in jobs.values()]
        fwait = sum(finished)
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(allwait, fwait, printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if all(finished):
            break

    ## check for errors in muscle_align_across
    keys = jobs.keys()
    for idx in keys:
        if not jobs[idx].successful():
            LOGGER.error("error in persistent_popen_align %s", jobs[idx].exception())
            raise IPyradWarningExit("error in step 6 {}".format(jobs[idx].exception()))
        del jobs[idx]
    print("")