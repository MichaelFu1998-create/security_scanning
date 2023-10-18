def run(data, samples, force, ipyclient):
    """ checks if the sample should be run and passes the args """
    ## prepare dirs
    data.dirs.consens = os.path.join(data.dirs.project, data.name+"_consens")
    if not os.path.exists(data.dirs.consens):
        os.mkdir(data.dirs.consens)

    ## zap any tmp files that might be leftover
    tmpcons = glob.glob(os.path.join(data.dirs.consens, "*_tmpcons.*"))
    tmpcats = glob.glob(os.path.join(data.dirs.consens, "*_tmpcats.*"))
    for tmpfile in tmpcons+tmpcats:
        os.remove(tmpfile)

    ## filter through samples for those ready
    samples = get_subsamples(data, samples, force)

    ## set up parallel client: how many cores?
    lbview = ipyclient.load_balanced_view()
    data.cpus = data._ipcluster["cores"]
    if not data.cpus:
        data.cpus = len(ipyclient.ids)

    ## wrap everything to ensure destruction of temp files
    inst = ""
    try:
        ## calculate depths, if they changed.
        samples = calculate_depths(data, samples, lbview)

        ## chunk clusters into bits for parallel processing
        lasyncs = make_chunks(data, samples, lbview)

        ## process chunks and cleanup
        process_chunks(data, samples, lasyncs, lbview)

    except KeyboardInterrupt as inst:
        raise inst

    finally:
        ## if process failed at any point delete tmp files
        tmpcons = glob.glob(os.path.join(data.dirs.clusts, "tmp_*.[0-9]*"))
        tmpcons += glob.glob(os.path.join(data.dirs.consens, "*_tmpcons.*"))
        tmpcons += glob.glob(os.path.join(data.dirs.consens, "*_tmpcats.*"))
        for tmpchunk in tmpcons:
            os.remove(tmpchunk)

        ## Finished step 5. Set step 6 checkpoint to 0 to force
        ## re-running from scratch.
        data._checkpoint = 0