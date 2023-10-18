def resolve_ambigs(tmpseq):
    """ 
    Randomly resolve ambiguous bases. This is applied to each boot
    replicate so that over reps the random resolutions don't matter.
    Sites are randomly resolved, so best for unlinked SNPs since 
    otherwise linked SNPs are losing their linkage information... 
    though it's not like we're using it anyways.
    """

    ## the order of rows in GETCONS
    for aidx in xrange(6):
        #np.uint([82, 75, 83, 89, 87, 77]):
        ambig, res1, res2 = GETCONS[aidx]

        ## get true wherever tmpseq is ambig
        idx, idy = np.where(tmpseq == ambig)
        halfmask = np.random.choice(np.array([True, False]), idx.shape[0])

        for col in xrange(idx.shape[0]):
            if halfmask[col]:
                tmpseq[idx[col], idy[col]] = res1
            else:
                tmpseq[idx[col], idy[col]] = res2
    return tmpseq