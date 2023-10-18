def cleanup(data, sample, statsdicts):
    """
    cleaning up. optim is the size (nloci) of tmp arrays
    """
    LOGGER.info("in cleanup for: %s", sample.name)
    isref = 'reference' in data.paramsdict["assembly_method"]

    ## collect consens chunk files
    combs1 = glob.glob(os.path.join(
                        data.dirs.consens,
                        sample.name+"_tmpcons.*"))
    combs1.sort(key=lambda x: int(x.split(".")[-1]))

    ## collect tmpcat files
    tmpcats = glob.glob(os.path.join(
                        data.dirs.consens,
                        sample.name+"_tmpcats.*"))
    tmpcats.sort(key=lambda x: int(x.split(".")[-1]))

    ## get shape info from the first cat, (optim, maxlen, 4)
    with h5py.File(tmpcats[0], 'r') as io5:
        optim, maxlen, _ = io5['cats'].shape

    ## save as a chunked compressed hdf5 array
    handle1 = os.path.join(data.dirs.consens, sample.name+".catg")
    with h5py.File(handle1, 'w') as ioh5:
        nloci = len(tmpcats) * optim
        dcat = ioh5.create_dataset("catg", (nloci, maxlen, 4),
                                   dtype=np.uint32,
                                   chunks=(optim, maxlen, 4),
                                   compression="gzip")
        dall = ioh5.create_dataset("nalleles", (nloci, ),
                                   dtype=np.uint8,
                                   chunks=(optim, ),
                                   compression="gzip")
        ## only create chrom for reference-aligned data
        if isref:
            dchrom = ioh5.create_dataset("chroms", (nloci, 3), 
                                         dtype=np.int64, 
                                         chunks=(optim, 3), 
                                         compression="gzip")

        ## Combine all those tmp cats into the big cat
        start = 0
        for icat in tmpcats:
            io5 = h5py.File(icat, 'r')
            end = start + optim
            dcat[start:end] = io5['cats'][:]
            dall[start:end] = io5['alls'][:]
            if isref:
                dchrom[start:end] = io5['chroms'][:]
            start += optim
            io5.close()
            os.remove(icat)

    ## store the handle to the Sample
    sample.files.database = handle1

    ## record results
    xcounters = {"nconsens": 0,
                 "heteros": 0,
                 "nsites": 0}
    xfilters = {"depth": 0,
               "maxh": 0,
               "maxn": 0}

    ## merge finished consens stats
    for counters, filters in statsdicts:
        ## sum individual counters
        for key in xcounters:
            xcounters[key] += counters[key]
        for key in xfilters:
            xfilters[key] += filters[key]

    ## merge consens read files
    handle1 = os.path.join(data.dirs.consens, sample.name+".consens.gz")
    with gzip.open(handle1, 'wb') as out:
        for fname in combs1:
            with open(fname) as infile:
                out.write(infile.read()+"\n")
            os.remove(fname)
    sample.files.consens = [handle1]

    ## set Sample stats_dfs values
    if int(xcounters['nsites']):
        prop = int(xcounters["heteros"]) / float(xcounters['nsites'])
    else:
        prop = 0

    sample.stats_dfs.s5.nsites = int(xcounters["nsites"])
    sample.stats_dfs.s5.nhetero = int(xcounters["heteros"])
    sample.stats_dfs.s5.filtered_by_depth = xfilters['depth']
    sample.stats_dfs.s5.filtered_by_maxH = xfilters['maxh']
    sample.stats_dfs.s5.filtered_by_maxN = xfilters['maxn']
    sample.stats_dfs.s5.reads_consens = int(xcounters["nconsens"])
    sample.stats_dfs.s5.clusters_total = sample.stats_dfs.s3.clusters_total
    sample.stats_dfs.s5.heterozygosity = float(prop)

    ## set the Sample stats summary value
    sample.stats.reads_consens = int(xcounters["nconsens"])

    ## save state to Sample if successful
    if sample.stats.reads_consens:
        sample.stats.state = 5
    else:
        print("No clusters passed filtering in Sample: {}".format(sample.name))
    return sample