def fill_boot(seqarr, newboot, newmap, spans, loci):
    """ fills the new bootstrap resampled array """
    ## column index
    cidx = 0
  
    ## resample each locus
    for i in xrange(loci.shape[0]):
        
        ## grab a random locus's columns
        x1 = spans[loci[i]][0]
        x2 = spans[loci[i]][1]
        cols = seqarr[:, x1:x2]

        ## randomize columns within colsq
        cord = np.random.choice(cols.shape[1], cols.shape[1], replace=False)
        rcols = cols[:, cord]
        
        ## fill bootarr with n columns from seqarr
        ## the required length was already measured
        newboot[:, cidx:cidx+cols.shape[1]] = rcols

        ## fill bootmap with new map info
        newmap[cidx: cidx+cols.shape[1], 0] = i+1
        
        ## advance column index
        cidx += cols.shape[1]

    ## return the concatenated cols
    return newboot, newmap