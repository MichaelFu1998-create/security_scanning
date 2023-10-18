def nworker(data, chunk):
    """
    Worker to distribute work to jit funcs. Wraps everything on an 
    engine to run single-threaded to maximize efficiency for 
    multi-processing.
    """

    ## set the thread limit on the remote engine
    oldlimit = set_mkl_thread_limit(1)

    ## open seqarray view, the modified arr is in bootstarr
    with h5py.File(data.database.input, 'r') as io5:
        seqview = io5["bootsarr"][:]
        maparr = io5["bootsmap"][:, 0]
        smps = io5["quartets"][chunk:chunk+data._chunksize]

        ## create an N-mask array of all seq cols
        nall_mask = seqview[:] == 78

    ## init arrays to fill with results
    rquartets = np.zeros((smps.shape[0], 4), dtype=np.uint16)
    rinvariants = np.zeros((smps.shape[0], 16, 16), dtype=np.uint16)

    ## fill arrays with results as we compute them. This iterates
    ## over all of the quartet sets in this sample chunk. It would
    ## be nice to have this all numbified.
    for idx in xrange(smps.shape[0]):
        sidx = smps[idx]
        seqs = seqview[sidx]

        ## these axis calls cannot be numbafied, but I can't 
        ## find a faster way that is JIT compiled, and I've
        ## really, really, really tried. Tried again now that
        ## numba supports axis args for np.sum. Still can't 
        ## get speed improvements by numbifying this loop.
        nmask = np.any(nall_mask[sidx], axis=0)
        nmask += np.all(seqs == seqs[0], axis=0) 

        ## here are the jitted funcs
        bidx, invar = calculate(seqs, maparr, nmask, TESTS)

        ## store results
        rquartets[idx] = smps[idx][bidx]
        rinvariants[idx] = invar

    ## reset thread limit
    set_mkl_thread_limit(oldlimit)

    ## return results...
    return rquartets, rinvariants