def demux2(data, chunkfiles, cutters, longbar, matchdict, ipyclient):
    """ 
    Submit chunks to be sorted by the barmatch() function then 
    calls putstats().
    """

    ## parallel stuff, limit to 1/4 of available cores for RAM limits.
    start = time.time()
    printstr = ' sorting reads         | {} | s1 |'
    lbview = ipyclient.load_balanced_view(targets=ipyclient.ids[::4])

    ## store statcounters and async results in dicts
    perfile = {}
    filesort = {}
    total = 0
    done = 0 

    ## chunkfiles is a dict with {handle: chunkslist, ...}. The func barmatch
    ## writes results to samplename files with PID number, and also writes a 
    ## pickle for chunk specific results with fidx suffix, which it returns.
    for handle, rawtuplist in chunkfiles.items():
        ## get args for job
        for fidx, rawtuple in enumerate(rawtuplist):
            #handle = os.path.splitext(os.path.basename(rawtuple[0]))[0]
            args = (data, rawtuple, cutters, longbar, matchdict, fidx)

            ## submit the job
            async = lbview.apply(barmatch, *args)
            filesort[total] = (handle, async)
            total += 1

            ## get ready to receive stats: 'total', 'cutfound', 'matched'
            perfile[handle] = np.zeros(3, dtype=np.int)

    ## stats for each sample
    fdbars = {}
    fsamplehits = Counter()
    fbarhits = Counter()
    fmisses = Counter()
    ## a tuple to hold my dictionaries
    statdicts = perfile, fsamplehits, fbarhits, fmisses, fdbars

    ## wait for jobs to finish
    while 1:
        fin = [i for i, j in filesort.items() if j[1].ready()]
        #fin = [i for i in jobs if i[1].ready()]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(total, done, printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)

        ## should we break?
        if total == done:
            print("")
            break

        ## cleanup
        for key in fin:
            tup = filesort[key]
            if tup[1].successful():
                pfile = tup[1].result()
                handle = tup[0]
                if pfile:
                    ## check if this needs to return data
                    putstats(pfile, handle, statdicts)
                    ## purge to conserve memory
                    del filesort[key]
                    done += 1

    return statdicts