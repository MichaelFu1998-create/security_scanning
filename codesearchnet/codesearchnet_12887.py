def demux(data, chunkfiles, cutters, longbar, matchdict, ipyclient):
    """ submit chunks to be sorted """

    ## parallel stuff
    start = time.time()
    printstr = ' sorting reads         | {} | s1 |'
    lbview = ipyclient.load_balanced_view()

    ## store statcounters and async results in dicts
    perfile = {}
    filesort = {}
    for handle, rawtuplist in chunkfiles.items():
        ## get args for job
        for fidx, rawtuple in enumerate(rawtuplist):
            #handle = os.path.splitext(os.path.basename(rawtuple[0]))[0]
            args = (data, rawtuple, cutters, longbar, matchdict, fidx)

            ## submit the job
            filesort[handle] = lbview.apply(barmatch, *args)

            ## get ready to receive stats: 'total', 'cutfound', 'matched'
            perfile[handle] = np.zeros(3, dtype=np.int)

    ## stats for each sample
    fdbars = {}
    fsamplehits = Counter()
    fbarhits = Counter()
    fmisses = Counter()
    ## a tuple to hold my dictionaries
    statdicts = perfile, fsamplehits, fbarhits, fmisses, fdbars

    try:
        kbd = 0
        total = len(chunkfiles)
        done = 0
        ## wait for jobs to finish
        while 1:
            fin = [i for i, j in filesort.items() if j.ready()]
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            progressbar(total, done, printstr.format(elapsed), spacer=data._spacer)
            time.sleep(0.1)

            ## should we break?
            if total == done:
                print("")
                break

            ## cleanup
            for job in fin:
                if filesort[job].successful():
                    pfile = filesort[job].result()
                    #if result:
                    if pfile:
                        ## check if this needs to return data
                        putstats(pfile, handle, statdicts)
                        
                        ## purge to conserve memory
                        del filesort[job]
                        done += 1

        ## keep tacking progreess during writing stage
        start = time.time()
        printstr = ' writing/compressing   | {} | s1 |'
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(10, 0, printstr.format(elapsed), spacer=data._spacer)


    except KeyboardInterrupt:
        ## wait to cleanup
        kbd = 1
        raise


    ## only proceed here if barmatch jobs were not interrupted
    else:
        ## collate files and do progress bar
        ftmps = glob.glob(os.path.join(data.dirs.fastqs, "tmp_*.fastq"))

        ## a dict to assign tmp files to names/reads
        r1dict = {}
        r2dict = {}
        for sname in data.barcodes:
            r1dict[sname] = []
            r2dict[sname] = []

        ## assign to name keys
        for ftmp in ftmps:
            ## split names
            base, orient, _ = ftmp.rsplit("_", 2)
            sname = base.rsplit("/", 1)[-1].split("tmp_", 1)[1]
            ## put into dicts
            if orient == "R1":
                r1dict[sname].append(ftmp)
            else:
                r2dict[sname].append(ftmp)

        ## concatenate files
        total = len(data.barcodes)
        done = 0

        ## store asyncs of collate jobs
        writers = []
        for sname in data.barcodes:
            tmp1s = sorted(r1dict[sname])
            tmp2s = sorted(r2dict[sname])
            writers.append(lbview.apply(collate_files, 
                           *[data, sname, tmp1s, tmp2s]))
        
        ## track progress of collate jobs
        while 1:
            ready = [i.ready() for i in writers]
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            progressbar(total, sum(ready), printstr.format(elapsed), spacer=data._spacer)  
            time.sleep(0.1)
            if all(ready):
                print("")
                break

    finally:
        ## clean up junk files
        tmpfiles = glob.glob(os.path.join(data.dirs.fastqs, "tmp_*_R*.fastq"))
        tmpfiles += glob.glob(os.path.join(data.dirs.fastqs, "tmp_*.p"))
        for tmpf in tmpfiles:
            os.remove(tmpf)

        if kbd:
            raise KeyboardInterrupt()
        else:
            ## build stats from dictionaries
            perfile, fsamplehits, fbarhits, fmisses, fdbars = statdicts    
            make_stats(data, perfile, fsamplehits, fbarhits, fmisses, fdbars)