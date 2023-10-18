def filter_stacks(data, sidx, hslice):
    """
    Grab a chunk of loci from the HDF5 database. Apply filters and fill the
    the filters boolean array.

    The design of the filtering steps intentionally sacrifices some performance
    for an increase in readability, and extensibility. Calling multiple filter
    functions ends up running through the sequences per stack several times,
    but I felt this design made more sense, and also will easily allow us to
    add more filters in the future.
    """
    LOGGER.info("Entering filter_stacks")

    ## open h5 handles
    io5 = h5py.File(data.clust_database, 'r')
    co5 = h5py.File(data.database, 'r')
    ## get a chunk (hslice) of loci for the selected samples (sidx)
    #superseqs = io5["seqs"][hslice[0]:hslice[1], sidx,]
    ## get an int view of the seq array
    #superints = io5["seqs"][hslice[0]:hslice[1], sidx, :].view(np.int8)

    ## we need to use upper to skip lowercase allele storage
    ## this slows down the rate of loading in data by a ton.
    superints = np.char.upper(io5["seqs"][hslice[0]:hslice[1], sidx,]).view(np.int8)
    LOGGER.info("superints shape {}".format(superints.shape))

    ## fill edge filter
    ## get edges of superseqs and supercats, since edges need to be trimmed
    ## before counting hets, snps, inds. Technically, this could edge trim
    ## clusters to the point that they are below the minlen, and so this
    ## also constitutes a filter, though one that is uncommon. For this
    ## reason we have another filter called edgfilter.
    splits = co5["edges"][hslice[0]:hslice[1], 4]
    edgfilter, edgearr = get_edges(data, superints, splits)
    del splits
    LOGGER.info('passed edges %s', hslice[0])

    ## minsamp coverages filtered from superseqs
    minfilter = filter_minsamp(data, superints)
    LOGGER.info('passed minfilt %s', hslice[0])

    ## maxhets per site column from superseqs after trimming edges
    hetfilter = filter_maxhet(data, superints, edgearr)
    LOGGER.info('passed minhet %s', hslice[0])

    ## ploidy filter
    pldfilter = io5["nalleles"][hslice[0]:hslice[1]].max(axis=1) > \
                                         data.paramsdict["max_alleles_consens"]

    ## indel filter, needs a fresh superints b/c get_edges does (-)->(N)
    indfilter = filter_indels(data, superints, edgearr)
    LOGGER.info('passed minind %s', hslice[0])

    ## Build the .loci snpstring as an array (snps)
    ## shape = (chunk, 1) dtype=S1, or should it be (chunk, 2) for [-,*] ?
    snpfilter, snpsarr = filter_maxsnp(data, superints, edgearr)

    LOGGER.info("edg %s", edgfilter.sum())
    LOGGER.info("min %s", minfilter.sum())
    LOGGER.info("het %s", hetfilter.sum())
    LOGGER.info("pld %s", pldfilter.sum())
    LOGGER.info("snp %s", snpfilter.sum())
    LOGGER.info("ind %s", indfilter.sum())

    ## SAVE FILTERS AND INFO TO DISK BY SLICE NUMBER (.0.tmp.h5)
    chunkdir = os.path.join(data.dirs.outfiles, data.name+"_tmpchunks")

    handle = os.path.join(chunkdir, "edgf.{}.npy".format(hslice[0]))
    with open(handle, 'w') as out:
        np.save(out, edgfilter)

    handle = os.path.join(chunkdir, "minf.{}.npy".format(hslice[0]))
    with open(handle, 'w') as out:
        np.save(out, minfilter)

    handle = os.path.join(chunkdir, "hetf.{}.npy".format(hslice[0]))
    with open(handle, 'w') as out:
        np.save(out, hetfilter)

    handle = os.path.join(chunkdir, "snpf.{}.npy".format(hslice[0]))
    with open(handle, 'w') as out:
        np.save(out, snpfilter)

    handle = os.path.join(chunkdir, "pldf.{}.npy".format(hslice[0]))
    with open(handle, 'w') as out:
        np.save(out, pldfilter)

    handle = os.path.join(chunkdir, "indf.{}.npy".format(hslice[0]))
    with open(handle, 'w') as out:
        np.save(out, indfilter)

    handle = os.path.join(chunkdir, "snpsarr.{}.npy".format(hslice[0]))
    with open(handle, 'w') as out:
        np.save(out, snpsarr)

    handle = os.path.join(chunkdir, "edgearr.{}.npy".format(hslice[0]))
    with open(handle, 'w') as out:
        np.save(out, edgearr)

    io5.close()
    co5.close()