def make_loci_and_stats(data, samples, ipyclient):
    """
    Makes the .loci file from h5 data base. Iterates by optim loci at a
    time and write to file. Also makes alleles file if requested.
    """
    ## start vcf progress bar
    start = time.time()
    printstr = " building loci/stats   | {} | s7 |"
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(20, 0, printstr.format(elapsed), spacer=data._spacer)

    ## get some db info
    with h5py.File(data.clust_database, 'r') as io5:
        ## will iterate optim loci at a time
        optim = io5["seqs"].attrs["chunksize"][0]
        nloci = io5["seqs"].shape[0]
        anames = io5["seqs"].attrs["samples"]

    ## get name and snp padding
    pnames, snppad = padnames(anames)
    snames = [i.name for i in samples]
    smask = np.array([i not in snames for i in anames])

    ## keep track of how many loci from each sample pass all filters
    samplecov = np.zeros(len(anames), dtype=np.int32)

    ## set initial value to zero for all values above min_samples_locus
    #for cov in range(data.paramsdict["min_samples_locus"], len(anames)+1):
    locuscov = Counter()
    for cov in range(len(anames)+1):
        locuscov[cov] = 0

    ## client for sending jobs to parallel engines
    lbview = ipyclient.load_balanced_view()

    ## send jobs in chunks
    loci_asyncs = {}
    for istart in xrange(0, nloci, optim):
        args = [data, optim, pnames, snppad, smask, istart, samplecov, locuscov, 1]
        loci_asyncs[istart] = lbview.apply(locichunk, args)

    while 1:
        done = [i.ready() for i in loci_asyncs.values()]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(len(done), sum(done), printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if len(done) == sum(done):
            print("")
            break

    ## check for errors
    for job in loci_asyncs:
        if loci_asyncs[job].ready() and not loci_asyncs[job].successful():
            LOGGER.error("error in building loci [%s]: %s",
                         job, loci_asyncs[job].exception())
            raise IPyradWarningExit(loci_asyncs[job].exception())

    ## concat and cleanup
    results = [i.get() for i in loci_asyncs.values()]
    ## update dictionaries
    for chunk in results:
        samplecov += chunk[0]
        locuscov.update(chunk[1])

    ## get all chunk files
    tmploci = glob.glob(data.outfiles.loci+".[0-9]*")
    ## sort by start value
    tmploci.sort(key=lambda x: int(x.split(".")[-1]))

    ## write tmpchunks to locus file
    locifile = open(data.outfiles.loci, 'w')
    for tmploc in tmploci:
        with open(tmploc, 'r') as inloc:
            locdat = inloc.read()
            locifile.write(locdat)
            os.remove(tmploc)
    locifile.close()

    ## make stats file from data
    make_stats(data, samples, samplecov, locuscov)

    ## repeat for alleles output
    if "a" in data.paramsdict["output_formats"]:

        loci_asyncs = {}
        for istart in xrange(0, nloci, optim):
            args = [data, optim, pnames, snppad, smask, istart, samplecov, locuscov, 0]
            loci_asyncs[istart] = lbview.apply(locichunk, args)

        while 1:
            done = [i.ready() for i in loci_asyncs.values()]
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            progressbar(len(done), sum(done),
                " building alleles      | {} | s7 |".format(elapsed), 
                spacer=data._spacer)
            time.sleep(0.1)
            if len(done) == sum(done):
                print("")
                break

        ## check for errors
        for job in loci_asyncs:
            if loci_asyncs[job].ready() and not loci_asyncs[job].successful():
                LOGGER.error("error in building alleles [%s]: %s",
                             job, loci_asyncs[job].exception())
                raise IPyradWarningExit(loci_asyncs[job].exception())

        ## concat and cleanup
        #results = [i.get() for i in loci_asyncs.values()]

        ## get all chunk files
        tmploci = glob.glob(data.outfiles.loci+".[0-9]*")
        ## sort by start value
        tmploci.sort(key=lambda x: int(x.split(".")[-1]))

        ## write tmpchunks to locus file
        locifile = open(data.outfiles.alleles, 'w')
        for tmploc in tmploci:
            with open(tmploc, 'r') as inloc:
                locdat = inloc.read()
                inalleles = get_alleles(locdat)
                locifile.write(inalleles)
                os.remove(tmploc)
        locifile.close()