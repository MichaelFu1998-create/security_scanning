def filter_maxhet(data, superints, edgearr):
    """
    Filter max shared heterozygosity per locus. The dimensions of superseqs
    are (chunk, sum(sidx), maxlen). Don't need split info since it applies to
    entire loci based on site patterns (i.e., location along the seq doesn't
    matter.) Current implementation does ints, but does not apply float diff
    to every loc based on coverage...
    """
    ## the filter max
    ## The type of max_shared_Hs_locus is determined and the cast to either
    ## int or float is made at assembly load time
    maxhet = data.paramsdict["max_shared_Hs_locus"]
    if isinstance(maxhet, float):
        ## get an array with maxhet fraction * ntaxa with data for each locus
        #maxhet = np.array(superints.shape[1]*maxhet, dtype=np.int16)
        maxhet = np.floor(
            maxhet * (superints.shape[1] - 
                np.all(superints == 78, axis=2).sum(axis=1))).astype(np.int16)
    elif isinstance(maxhet, int):
        maxhet = np.zeros(superints.shape[0], dtype=np.int16)
        maxhet.fill(data.paramsdict["max_shared_Hs_locus"])

    ## an empty array to fill with failed loci
    LOGGER.info("--------------maxhet mins %s", maxhet)
    hetfilt = np.zeros(superints.shape[0], dtype=np.bool)
    hetfilt = maxhet_numba(superints, edgearr, maxhet, hetfilt)
    LOGGER.info("--------------maxhet sums %s", hetfilt.sum())
    return hetfilt