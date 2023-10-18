def get_seeds_and_hits(uhandle, bseeds, snames):
    """
    builds a seeds and hits (uarr) array of ints from the utemp.sort file.
    Saves outputs to files ...
    """
    ## Get max name length. Allow for trailing _ + up to 9 digits
    ## of numbers of loci (an astronomical number of unique loci)
    maxlen_names = np.max(map(len, snames)) + 10
    ## read in the utemp.sort file
    updf = np.loadtxt(uhandle, dtype="S".format(maxlen_names))

    ## Get seeds for all matches from usort
    seeds = np.unique(updf[:, 1])
    seedsarr = np.column_stack([
                    np.arange(len(seeds)),
                   [i.rsplit("_", 1)[0] for i in seeds],
                   [i.rsplit("_", 1)[1] for i in seeds]])
    seedsarr[:, 1] = [snames.index(i) for i in seedsarr[:, 1]]
    seedsarr = seedsarr.astype(np.int64)
    LOGGER.info("got a seedsarr %s", seedsarr.shape)

    ## Get matches from usort and create an array for fast entry
    uarr = np.zeros((updf.shape[0], 3), dtype=np.int64)
    idx = -1
    lastloc = None
    for ldx in xrange(updf.shape[0]):
        tloc = updf[ldx, 1]
        if tloc != lastloc:
            idx += 1
        uarr[ldx, 0] = idx
        lastloc = tloc
    ## create a column with sample index
    uarr[:, 1] = [int(snames.index(i.rsplit("_", 1)[0])) for i in updf[:, 0]]
    ## create a column with only consens index for sample
    uarr[:, 2] = [int(i.rsplit("_", 1)[1]) for i in updf[:, 0]]
    uarr = uarr.astype(np.int64)
    LOGGER.info("got a uarr %s", uarr.shape)

    ## save as h5 to we can grab by sample slices
    with h5py.File(bseeds, 'w') as io5:
        io5.create_dataset("seedsarr", data=seedsarr, dtype=np.int64)
        io5.create_dataset("uarr", data=uarr, dtype=np.int64)