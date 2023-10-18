def batch(
    baba,
    ipyclient=None,
    ):
    """
    distributes jobs to the parallel client
    """

    ## parse args
    handle = baba.data
    taxdicts = baba.tests
    mindicts = baba.params.mincov
    nboots = baba.params.nboots

    ## if ms generator make into reusable list
    sims = 0
    if isinstance(handle, types.GeneratorType):
        handle = list(handle)
        sims = 1
    else:
        ## expand locifile path to full path
        handle = os.path.realpath(handle)

    ## parse taxdicts into names and lists if it a dictionary
    #if isinstance(taxdicts, dict):
    #    names, taxdicts = taxdicts.keys(), taxdicts.values()
    #else:
    #    names = []
    names = []
    if isinstance(taxdicts, dict):
        taxdicts = [taxdicts]

    ## an array to hold results (len(taxdicts), nboots)
    tot = len(taxdicts)
    resarr = np.zeros((tot, 7), dtype=np.float64)
    bootsarr = np.zeros((tot, nboots), dtype=np.float64)
    paneldict = {}

    ## TODO: Setup a wrapper to find and cleanup ipyclient
    ## define the function and parallelization to use, 
    ## if no ipyclient then drops back to using multiprocessing.
    if not ipyclient:
        # ipyclient = ip.core.parallel.get_client(**self._ipcluster)
        raise IPyradError("you must enter an ipyparallel.Client() object")
    else:
        lbview = ipyclient.load_balanced_view()

    ## submit jobs to run on the cluster queue
    start = time.time()
    asyncs = {}
    idx = 0

    ## prepare data before sending to engines
    ## if it's a str (locifile) then parse it here just once.
    if isinstance(handle, str):
        with open(handle, 'r') as infile:
            loci = infile.read().strip().split("|\n")
    if isinstance(handle, list):
        pass #sims()

    ## iterate over tests (repeats mindicts if fewer than taxdicts)
    itests = iter(taxdicts)
    imdict = itertools.cycle([mindicts])

    #for test, mindict in zip(taxdicts, itertools.cycle([mindicts])):
    for i in xrange(len(ipyclient)):

        ## next entries unless fewer than len ipyclient, skip
        try:
            test = next(itests)
            mindict = next(imdict)
        except StopIteration:
            continue

        ## if it's sim data then convert to an array
        if sims:
            loci = _msp_to_arr(handle, test)
            args = (loci, test, mindict, nboots)
            print("not yet implemented")
            #asyncs[idx] = lbview.apply_async(dstat, *args)
        else:
            args = [loci, test, mindict, nboots]
            asyncs[idx] = lbview.apply(dstat, *args)
        idx += 1

    ## block until finished, print progress if requested.
    finished = 0
    try:
        while 1:
            keys = [i for (i, j) in asyncs.items() if j.ready()]
            ## check for failures
            for job in keys:
                if not asyncs[job].successful():
                    raise IPyradWarningExit(\
                        " error: {}: {}".format(job, asyncs[job].exception()))
                ## enter results for successful jobs
                else:
                    _res, _bot = asyncs[job].result()
                    
                    ## store D4 results
                    if _res.shape[0] == 1:
                        resarr[job] = _res.T.as_matrix()[:, 0]
                        bootsarr[job] = _bot
                    
                    ## or store D5 results                        
                    else:   
                        paneldict[job] = _res.T

                    ## remove old job
                    del asyncs[job]
                    finished += 1

                    ## submit next job if there is one.
                    try:
                        test = next(itests)
                        mindict = next(imdict)
                        if sims:
                            loci = _msp_to_arr(handle, test)
                            args = (loci, test, mindict, nboots)
                            print("not yet implemented")
                            #asyncs[idx] = lbview.apply_async(dstat, *args)
                        else:
                            args = [loci, test, mindict, nboots]
                            asyncs[idx] = lbview.apply(dstat, *args)
                        idx += 1
                    except StopIteration:
                        pass

            ## count finished and break if all are done.
            #fin = idx - len(asyncs)
            elap = datetime.timedelta(seconds=int(time.time()-start))
            printstr = " calculating D-stats  | {} | "
            progressbar(tot, finished, printstr.format(elap), spacer="")
            time.sleep(0.1)
            if not asyncs:
                print("")
                break

    except KeyboardInterrupt as inst:
        ## cancel all jobs (ipy & multiproc modes) and then raise error
        try:
            ipyclient.abort()
        except Exception:
            pass
        raise inst

    ## dress up resarr as a Pandas DataFrame if 4-part test
    if len(test) == 4:
        if not names:
            names = range(len(taxdicts))
        #print("resarr")
        #print(resarr)
        resarr = pd.DataFrame(resarr, 
            index=names,
            columns=["dstat", "bootmean", "bootstd", "Z", "ABBA", "BABA", "nloci"])

        ## sort results and bootsarr to match if test names were supplied
        resarr = resarr.sort_index()
        order = [list(resarr.index).index(i) for i in names]
        bootsarr = bootsarr[order]
        return resarr, bootsarr
    else:
        ## order results dfs
        listres = []
        for key in range(len(paneldict)):
            listres.append(paneldict[key])
            
        ## make into a multi-index dataframe
        ntests = len(paneldict)
        multi_index = [
            np.array([[i] * 3 for i in range(ntests)]).flatten(),
            np.array(['p3', 'p4', 'shared'] * ntests),
        ]
        resarr = pd.DataFrame(
            data=pd.concat(listres).as_matrix(), 
            index=multi_index,
            columns=listres[0].columns,
            )
        return resarr, None