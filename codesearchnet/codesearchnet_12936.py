def clean_and_build_concat(data, samples, randomseed, ipyclient):
    """ 
    STEP 6-1:
    Clears dirs and databases and calls 'build_input_file()'
    """
    ## but check for new clust database name if this is a new branch
    cleanup_tempfiles(data)
    catclust = os.path.join(data.dirs.across, data.name+"_catclust.gz")
    if os.path.exists(catclust):
        os.remove(catclust)
    if os.path.exists(data.clust_database):
        os.remove(data.clust_database)

    ## get parallel view
    start = time.time()
    printstr = " concat/shuffle input  | {} | s6 |"

    ## make a vsearch input fasta file with all samples reads concat
    async = ipyclient[0].apply(build_input_file, *[data, samples, randomseed])
    while 1:
        ready = int(async.ready())
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(1, ready, printstr.format(elapsed), spacer=data._spacer)
        if ready:
            break
        else:
            time.sleep(0.1)
    print("")

    ## store that this step was successful
    if not async.successful():
        raise IPyradWarningExit(async.result())