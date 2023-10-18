def make_vcf(data, samples, ipyclient, full=0):
    """
    Write the full VCF for loci passing filtering. Other vcf formats are
    possible, like SNPs-only, or with filtered loci included but the filter
    explicitly labeled. These are not yet supported, however.
    """
    ## start vcf progress bar
    start = time.time()
    printstr = " building vcf file     | {} | s7 |"
    LOGGER.info("Writing .vcf file")
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(20, 0, printstr.format(elapsed), spacer=data._spacer)

    ## create outputs for v and V, gzip V to be friendly
    data.outfiles.vcf = os.path.join(data.dirs.outfiles, data.name+".vcf")
    if full:
        data.outfiles.VCF = os.path.join(data.dirs.outfiles, data.name+".vcf.gz")

    ## get some db info
    with h5py.File(data.clust_database, 'r') as io5:
        ## will iterate optim loci at a time
        optim = io5["seqs"].attrs["chunksize"][0]
        nloci = io5["seqs"].shape[0]
        ## get name and snp padding
        anames = io5["seqs"].attrs["samples"]
        snames = [i.name for i in samples]
        names = [i for i in anames if i in snames]

    ## get names index
    sidx = np.array([i in snames for i in anames])

    ## client for sending jobs to parallel engines, for this step we'll limit
    ## to half of the available cpus if
    lbview = ipyclient.load_balanced_view()

    ## send jobs in chunks
    vasyncs = {}
    total = 0
    for chunk in xrange(0, nloci, optim):
        vasyncs[chunk] = lbview.apply(vcfchunk, *(data, optim, sidx, chunk, full))
        total += 1

    ## tmp files get left behind and intensive processes are left running when a
    ## a job is killed/interrupted during vcf build, so we try/except wrap.
    try:
        while 1:
            keys = [i for (i, j) in vasyncs.items() if j.ready()]
            ## check for failures
            for job in keys:
                if not vasyncs[job].successful():
                    ## raise exception
                    err = " error in vcf build chunk {}: {}"\
                          .format(job, vasyncs[job].result())
                    LOGGER.error(err)
                    raise IPyradWarningExit(err)
                else:
                    ## free up memory
                    del vasyncs[job]

            finished = total - len(vasyncs) #sum([i.ready() for i in vasyncs.values()])
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            progressbar(total, finished, printstr.format(elapsed), spacer=data._spacer)
            time.sleep(0.5)
            if not vasyncs:
                break
        print("")

    except Exception as inst:
        ## make sure all future jobs are aborted
        keys = [i for (i, j) in vasyncs.items() if not j.ready()]
        try:
            for job in keys:
                #vasyncs[job].abort()
                vasyncs[job].cancel()
        except Exception:
            pass
        ## make sure all tmp files are destroyed
        vcfchunks = glob.glob(os.path.join(data.dirs.outfiles, "*.vcf.[0-9]*"))
        h5chunks = glob.glob(os.path.join(data.dirs.outfiles, ".tmp.[0-9]*.h5"))
        for dfile in vcfchunks+h5chunks:
            os.remove(dfile)
        ## reraise the error
        raise inst


    ## writing full vcf file to disk
    start = time.time()
    printstr = " writing vcf file      | {} | s7 |"
    res = lbview.apply(concat_vcf, *(data, names, full))
    ogchunks = len(glob.glob(data.outfiles.vcf+".*"))
    while 1:
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        curchunks = len(glob.glob(data.outfiles.vcf+".*"))
        progressbar(ogchunks, ogchunks-curchunks, printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if res.ready():
            break
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(1, 1, printstr.format(elapsed), spacer=data._spacer)
    print("")