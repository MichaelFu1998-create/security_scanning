def nworker(data, smpchunk, tests):
    """ The workhorse function. Not numba. """
    
    ## tell engines to limit threads
    #numba.config.NUMBA_DEFAULT_NUM_THREADS = 1
    
    ## open the seqarray view, the modified array is in bootsarr
    with h5py.File(data.database.input, 'r') as io5:
        seqview = io5["bootsarr"][:]
        maparr = io5["bootsmap"][:]

    ## create an N-mask array of all seq cols (this isn't really too slow)
    nall_mask = seqview[:] == 78

    ## tried numba compiling everythign below here, but was not faster
    ## than making nmask w/ axis arg in numpy

    ## get the input arrays ready
    rquartets = np.zeros((smpchunk.shape[0], 4), dtype=np.uint16)
    rweights = None
    #rweights = np.ones(smpchunk.shape[0], dtype=np.float64)
    rdstats = np.zeros((smpchunk.shape[0], 4), dtype=np.uint32)

    #times = []
    ## fill arrays with results using numba funcs
    for idx in xrange(smpchunk.shape[0]):
        ## get seqchunk for 4 samples (4, ncols) 
        sidx = smpchunk[idx]
        seqchunk = seqview[sidx]

        ## get N-containing columns in 4-array, and invariant sites.
        nmask = np.any(nall_mask[sidx], axis=0)
        nmask += np.all(seqchunk == seqchunk[0], axis=0)  ## <- do we need this?

        ## get matrices if there are any shared SNPs
        ## returns best-tree index, qscores, and qstats
        #bidx, qscores, qstats = calculate(seqchunk, maparr[:, 0], nmask, tests)
        bidx, qstats = calculate(seqchunk, maparr[:, 0], nmask, tests)
        
        ## get weights from the three scores sorted. 
        ## Only save to file if the quartet has information
        rdstats[idx] = qstats 
        rquartets[idx] = smpchunk[idx][bidx]

    return rquartets, rweights, rdstats