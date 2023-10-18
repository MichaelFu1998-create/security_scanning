def filter_all_clusters(data, samples, ipyclient):
    """
    Open the clust_database HDF5 array with seqs, catg, and filter data. 
    Fill the remaining filters.
    """
    ## create loadbalanced ipyclient
    lbview = ipyclient.load_balanced_view()

    ## get chunk size from the HD5 array and close
    with h5py.File(data.clust_database, 'r') as io5:
        ## the size of chunks for reading/writing
        optim = io5["seqs"].attrs["chunksize"][0]
        ## the samples in the database in their locus order
        dbsamples = io5["seqs"].attrs["samples"]
        ## the total number of loci
        nloci = io5["seqs"].shape[0]

    ## make a tmp directory for saving chunked arrays to
    chunkdir = os.path.join(data.dirs.outfiles, data.name+"_tmpchunks")
    if not os.path.exists(chunkdir):
        os.mkdir(chunkdir)

    ## get the indices of the samples that we are going to include
    sidx = select_samples(dbsamples, samples)
    ## do the same for the populations samples
    if data.populations:
        data._populations = {}
        for pop in data.populations:
            try:
                _samps = [data.samples[i] for i in data.populations[pop][1]]
                data._populations[pop] = (
                    data.populations[pop][0],
                    select_samples(dbsamples, _samps, sidx))
            except:
                print("    Sample in populations file not present in assembly - {}".format(data.populations[pop][1]))
                raise
                                                
    LOGGER.info("samples %s \n, dbsamples %s \n, sidx %s \n",
                samples, dbsamples, sidx)

    ## Put inside a try statement so we can delete tmpchunks
    try:
        ## load a list of args to send to Engines. Each arg contains the index
        ## to sample optim loci from catg, seqs, filters &or edges, which will
        ## be loaded on the remote Engine.

        ## create job queue
        start = time.time()
        printstr = " filtering loci        | {} | s7 |"
        fasyncs = {}
        submitted = 0
        while submitted < nloci:
            hslice = np.array([submitted, submitted+optim])
            fasyncs[hslice[0]] = lbview.apply(filter_stacks, *(data, sidx, hslice))
            submitted += optim

        ## run filter_stacks on all chunks
        while 1:
            readies = [i.ready() for i in fasyncs.values()]
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            progressbar(len(readies), sum(readies),
                printstr.format(elapsed), spacer=data._spacer)
            time.sleep(0.1)
            if sum(readies) == len(readies):
                print("")
                break

        ## raise error if any jobs failed
        for async in fasyncs:
            if not fasyncs[async].successful():
                LOGGER.error("error in filter_stacks on chunk %s: %s",
                             async, fasyncs[async].exception())
                raise IPyradWarningExit("error in filter_stacks on chunk {}: {}"\
                             .format(async, fasyncs[async].exception()))
        ipyclient.purge_everything()

        ## get all the saved tmp arrays for each slice
        tmpsnp = glob.glob(os.path.join(chunkdir, "snpf.*.npy"))
        tmphet = glob.glob(os.path.join(chunkdir, "hetf.*.npy"))
        tmpmin = glob.glob(os.path.join(chunkdir, "minf.*.npy"))
        tmpedg = glob.glob(os.path.join(chunkdir, "edgf.*.npy"))
        tmppld = glob.glob(os.path.join(chunkdir, "pldf.*.npy"))
        tmpind = glob.glob(os.path.join(chunkdir, "indf.*.npy"))

        ## sort array files within each group
        arrdict = OrderedDict([('ind', tmpind),
                               ('snp', tmpsnp), ('het', tmphet),
                               ('min', tmpmin), ('edg', tmpedg),
                               ('pld', tmppld)])
        for arrglob in arrdict.values():
            arrglob.sort(key=lambda x: int(x.rsplit(".")[-2]))

        ## re-load the full filter array who's order is
        ## ["duplicates", "max_indels", "max_snps", "max_hets", "min_samps", "max_alleles"]
        io5 = h5py.File(data.database, 'r+')
        superfilter = np.zeros(io5["filters"].shape, io5["filters"].dtype)

        ## iterate across filter types (dups is already filled)
        ## we have [4,4] b/c minf and edgf both write to minf
        for fidx, ftype in zip([1, 2, 3, 4, 4, 5], arrdict.keys()):
            ## fill in the edgefilters
            for ffile in arrdict[ftype]:
                ## grab a file and get it's slice
                hslice = int(ffile.split(".")[-2])
                ## load in the array
                arr = np.load(ffile)
                ## store slice into full array (we use += here because the minf
                ## and edgf arrays both write to the same filter).
                superfilter[hslice:hslice+optim, fidx] += arr

        ## store to DB
        io5["filters"][:] += superfilter
        del arr, superfilter

        ## store the other arrayed values (edges, snps)
        edgarrs = glob.glob(os.path.join(chunkdir, "edgearr.*.npy"))
        snparrs = glob.glob(os.path.join(chunkdir, "snpsarr.*.npy"))

        ## sort array files within each group
        arrdict = OrderedDict([('edges', edgarrs), ('snps', snparrs)])
        for arrglob in arrdict.values():
            arrglob.sort(key=lambda x: int(x.rsplit(".")[-2]))

        ## fill the edge array, splits are already in there.
        superedge = np.zeros(io5['edges'].shape, io5['edges'].dtype)
        for ffile in arrdict['edges']:
            ## grab a file and get it's slice
            hslice = int(ffile.split(".")[-2])
            ## load in the array w/ shape (hslice, 5)
            arr = np.load(ffile)
            ## store slice into full array
            superedge[hslice:hslice+optim, :] = arr
        io5["edges"][:, :] = superedge
        del arr, superedge

        ## fill the snps array. shape= (nloci, maxlen, 2)
        supersnps = np.zeros(io5['snps'].shape, io5['snps'].dtype)
        for ffile in arrdict['snps']:
            ## grab a file and get it's slice
            hslice = int(ffile.split(".")[-2])
            ## load in the array w/ shape (hslice, maxlen, 2)
            arr = np.load(ffile)
            ## store slice into full array
            LOGGER.info("shapes, %s %s", supersnps.shape, arr.shape)
            supersnps[hslice:hslice+optim, :, :] = arr
        io5["snps"][:] = supersnps
        del arr
        io5.close()

    finally:
        ## clean up the tmp files/dirs even if we failed.
        try:
            LOGGER.info("finished filtering")
            shutil.rmtree(chunkdir)
        except (IOError, OSError):
            pass