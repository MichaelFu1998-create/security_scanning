def subsample_snps_map(seqchunk, nmask, maparr):
    """ 
    removes ncolumns from snparray prior to matrix calculation, and 
    subsamples 'linked' snps (those from the same RAD locus) such that
    for these four samples only 1 SNP per locus is kept. This information
    comes from the 'map' array (map file). 
    """
    ## mask columns that contain Ns
    rmask = np.zeros(seqchunk.shape[1], dtype=np.bool_)

    ## apply mask to the mapfile
    last_loc = -1
    for idx in xrange(maparr.shape[0]):
        if maparr[idx] != last_loc:
            if not nmask[idx]:
                rmask[idx] = True
            last_loc = maparr[idx]
    
    ## apply mask
    #newarr = seqchunk[:, rmask]
    
    ## return smaller Nmasked array
    return rmask