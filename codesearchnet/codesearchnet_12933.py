def build_clustbits(data, ipyclient, force):
    """
    Reconstitutes clusters from .utemp and htemp files and writes them
    to chunked files for aligning in muscle.
    """

    ## If you run this step then we clear all tmp .fa and .indel.h5 files
    if os.path.exists(data.tmpdir):
        shutil.rmtree(data.tmpdir)
        os.mkdir(data.tmpdir)

    ## parallel client
    lbview = ipyclient.load_balanced_view()
    start = time.time()
    printstr = " building clusters     | {} | s6 |"
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(3, 0, printstr.format(elapsed), spacer=data._spacer)

    uhandle = os.path.join(data.dirs.across, data.name+".utemp")
    usort = os.path.join(data.dirs.across, data.name+".utemp.sort")

    async1 = ""
    ## skip usorting if not force and already exists
    if not os.path.exists(usort) or force:

        ## send sort job to engines. Sorted seeds allows us to work through
        ## the utemp file one locus at a time instead of reading all into mem.
        LOGGER.info("building reads file -- loading utemp file into mem")
        async1 = lbview.apply(sort_seeds, *(uhandle, usort))
        while 1:
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            progressbar(3, 0, printstr.format(elapsed), spacer=data._spacer)
            if async1.ready():
                break
            else:
                time.sleep(0.1)

    ## send count seeds job to engines.
    async2 = lbview.apply(count_seeds, usort)
    while 1:
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(3, 1, printstr.format(elapsed), spacer=data._spacer)
        if async2.ready():
            break
        else:
            time.sleep(0.1)

    ## wait for both to finish while printing progress timer
    nseeds = async2.result()

    ## send the clust bit building job to work and track progress
    async3 = lbview.apply(sub_build_clustbits, *(data, usort, nseeds))
    while 1:
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(3, 2, printstr.format(elapsed), spacer=data._spacer)
        if async3.ready():
            break
        else:
            time.sleep(0.1)
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(3, 3, printstr.format(elapsed), spacer=data._spacer)
    print("")

    ## check for errors
    for job in [async1, async2, async3]:
        try:
            if not job.successful():
                raise IPyradWarningExit(job.result())
        except AttributeError:
            ## If we skip usorting then async1 == "" so the call to
            ## successful() raises, but we can ignore it.
            pass