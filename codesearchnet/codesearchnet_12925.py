def multicat(data, samples, ipyclient):
    """
    Runs singlecat and cleanup jobs for each sample.
    For each sample this fills its own hdf5 array with catg data & indels.
    This is messy, could use simplifiying.
    """

    ## progress ticker
    start = time.time()
    printstr = " indexing clusters     | {} | s6 |"
    elapsed = datetime.timedelta(seconds=int(time.time() - start))
    progressbar(20, 0, printstr.format(elapsed))

    ## parallel client
    lbview = ipyclient.load_balanced_view()

    ## First submit a sleeper job as temp_flag for cleanups
    last_sample = 0
    cleanups = {}
    cleanups[last_sample] = lbview.apply(time.sleep, 0.0)

    ## get samples and names, sorted
    snames = [i.name for i in samples]
    snames.sort()

    ## Build an array for quickly indexing consens reads from catg files.
    ## save as a npy int binary file.
    uhandle = os.path.join(data.dirs.across, data.name+".utemp.sort")
    bseeds = os.path.join(data.dirs.across, data.name+".tmparrs.h5")

    ## send as first async1 job
    async1 = lbview.apply(get_seeds_and_hits, *(uhandle, bseeds, snames))
    async2 = lbview.apply(fill_dups_arr, data)

    ## progress bar for seed/hit sorting
    while not (async1.ready() and async2.ready()):
        elapsed = datetime.timedelta(seconds=int(time.time() - start))
        progressbar(20, 0, printstr.format(elapsed))
        time.sleep(0.1)
    if not async1.successful():
        raise IPyradWarningExit("error in get_seeds: %s", async1.exception())
    if not async2.successful():
        raise IPyradWarningExit("error in fill_dups: %s", async2.exception())

    ## make a limited njobs view based on mem limits 
    ## is using smallview necessary? (yes, it is for bad libraries)
    smallview = ipyclient.load_balanced_view(targets=ipyclient.ids[::2])

    ## make sure there are no old tmp.h5 files 
    smpios = [os.path.join(data.dirs.across, sample.name+'.tmp.h5') \
              for sample in samples]
    for smpio in smpios:
        if os.path.exists(smpio):
            os.remove(smpio)

    ## send 'singlecat()' jobs to engines
    jobs = {}
    for sample in samples:
        sidx = snames.index(sample.name)
        jobs[sample.name] = smallview.apply(singlecat, *(data, sample, bseeds, sidx))

    ## check for finished and submit disk-writing job when finished
    alljobs = len(jobs)
    while 1:
        ## check for finished jobs
        curkeys = jobs.keys()
        for key in curkeys:
            async = jobs[key]
            if async.ready():
                if async.successful():
                    ## submit cleanup for finished job
                    args = (data, data.samples[key], snames.index(key))
                    with lbview.temp_flags(after=cleanups[last_sample]):
                        cleanups[key] = lbview.apply(write_to_fullarr, *args)
                    last_sample = key
                    del jobs[key]
                else:
                    err = jobs[key].exception()
                    errmsg = "singlecat error: {} {}".format(key, err)
                    raise IPyradWarningExit(errmsg)
        ## print progress or break
        elapsed = datetime.timedelta(seconds=int(time.time() - start))
        progressbar(alljobs, alljobs-len(jobs), printstr.format(elapsed))
        time.sleep(0.1)
        if not jobs:
            break

    ## add the dask_chroms func for reference data
    if 'reference' in data.paramsdict["assembly_method"]:
        with lbview.temp_flags(after=cleanups.values()):
            cleanups['ref'] = lbview.apply(dask_chroms, *(data, samples))

    ## wait for "write_to_fullarr" jobs to finish
    print("")
    start = time.time()
    printstr = " building database     | {} | s6 |"
    while 1:
        finished = [i for i in cleanups.values() if i.ready()]
        elapsed = datetime.timedelta(seconds=int(time.time() - start))
        progressbar(len(cleanups), len(finished), printstr.format(elapsed))
        time.sleep(0.1)
        ## break if one failed, or if finished
        if not all([i.successful() for i in finished]):
            break
        if len(cleanups) == len(finished):
            break

    ## check for errors
    for job in cleanups:
        if cleanups[job].ready():
            if not cleanups[job].successful():
                err = " error in write_to_fullarr ({}) {}"\
                     .format(job, cleanups[job].result())
                LOGGER.error(err)
                raise IPyradWarningExit(err)

    ## remove large indels array file and singlecat tmparr file
    ifile = os.path.join(data.dirs.across, data.name+".tmp.indels.hdf5")
    if os.path.exists(ifile):
        os.remove(ifile)
    if os.path.exists(bseeds):
        os.remove(bseeds)
    for sh5 in [os.path.join(data.dirs.across, i.name+".tmp.h5") for i in samples]:
        os.remove(sh5)

    ## print final progress
    elapsed = datetime.timedelta(seconds=int(time.time() - start))
    progressbar(10, 10, printstr.format(elapsed))
    print("")