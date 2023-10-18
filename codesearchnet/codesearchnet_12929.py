def inserted_indels(indels, ocatg):
    """
    inserts indels into the catg array
    """
    ## return copy with indels inserted
    newcatg = np.zeros(ocatg.shape, dtype=np.uint32)

    ## iterate over loci and make extensions for indels
    for iloc in xrange(ocatg.shape[0]):
        ## get indels indices
        indidx = np.where(indels[iloc, :])[0]
        if np.any(indidx):
            ## which new (empty) rows will be added
            allrows = np.arange(ocatg.shape[1])
            mask = np.ones(allrows.shape[0], dtype=np.bool_)
            for idx in indidx:
                mask[idx] = False
            not_idx = allrows[mask == 1]

            ## fill in new data into all other spots
            newcatg[iloc][not_idx] = ocatg[iloc, :not_idx.shape[0]]
        else:
            newcatg[iloc] = ocatg[iloc]
    return newcatg