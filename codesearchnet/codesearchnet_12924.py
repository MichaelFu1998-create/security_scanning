def new_multicat(data, samples, ipyclient):
    """
    Calls 'singlecat()' for all samples to build index files.
    """

    ## track progress
    LOGGER.info("in the multicat")
    start = time.time()
    printstr = " indexing clusters     | {} | s6 |"

    ## Build the large h5 array. This will write a new HDF5 file and overwrite
    ## existing data. 
    nloci = get_nloci(data)
    build_h5_array(data, samples, nloci)

    ## parallel client (reserve engine 0 for data entry), if/else here in case
    ## user has only one engine.
    if len(ipyclient) > 1:
        filler = ipyclient.load_balanced_view(targets=[0])
        smallview = ipyclient.load_balanced_view(targets=ipyclient.ids[1::2])
    else:
        filler = ipyclient.load_balanced_view(targets=[0])
        smallview = ipyclient.load_balanced_view(targets=[0])                

    ## First submit a sleeper job as temp_flag for cleanups
    last_sample = 0
    cleanups = {}
    cleanups[last_sample] = filler.apply(time.sleep, 0.0)

    ## fill the duplicates filter array
    async = smallview.apply(fill_dups_arr, data)
    while 1:
        elapsed = datetime.timedelta(seconds=int(time.time() - start))
        progressbar(20, 0, printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if async.ready():
            break
    if not async.successful():
        raise IPyradWarningExit(async.result())

    ## Get all existing .tmp.h5 files. If files exist then assume that we are
    ## restarting an interrupted job. We need to check for each one whether it 
    ## has it finished being built, and whether it has been written to the 
    ## large array yet.
    snames = [i.name for i in samples]
    snames.sort()
    smpios = {i:os.path.join(data.dirs.across, i+'.tmp.h5') for i in snames}

    ## send 'singlecat()' jobs to engines
    bseeds = os.path.join(data.dirs.across, data.name+".tmparrs.h5")
    jobs = {}
    for sample in samples:
        sidx = snames.index(sample.name)
        args = (data, sample, bseeds, sidx, nloci)

        ## Only build it if it doesn't already exist. Singlecat removes
        ## unfinished files if interrupted, so .tmp.h5 should not exist
        ## unless the file is ready to be entered. 
        if not os.path.exists(smpios[sample.name]):
            jobs[sample.name] = smallview.apply(singlecat, *args)

    ## track progress of singlecat jobs and submit writing jobs for finished
    ## singlecat files (.tmp.h5).
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
                    with filler.temp_flags(after=cleanups[last_sample]):
                        cleanups[key] = filler.apply(write_to_fullarr, *args)
                        last_sample = key
                        del jobs[key]
                else:
                    if not async.successful():
                        raise IPyradWarningExit(async.result())

        ## print progress or break
        elapsed = datetime.timedelta(seconds=int(time.time() - start))
        progressbar(alljobs, alljobs-len(jobs), printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if not jobs:
            break        

    ## add the dask_chroms func for reference data
    if 'reference' in data.paramsdict["assembly_method"]:
        with filler.temp_flags(after=cleanups.values()):
            cleanups['ref'] = filler.apply(dask_chroms, *(data, samples))

    ## ------- print breakline between indexing and writing database ---------
    print("")

    ## track progress of databaseing
    start = time.time()
    printstr = " building database     | {} | s6 |"
    while 1:
        finished = [i for i in cleanups.values() if i.ready()]
        elapsed = datetime.timedelta(seconds=int(time.time() - start))
        progressbar(len(cleanups), len(finished), printstr.format(elapsed), spacer=data._spacer)
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
                raise IPyradWarningExit((job, cleanups[job].result()))