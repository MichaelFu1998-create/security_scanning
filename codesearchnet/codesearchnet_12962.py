def resolve_ambigs(tmpseq):
    """ returns a seq array with 'RSKYWM' randomly replaced with resolved bases"""
    ## iterate over the bases 'RSKWYM': [82, 83, 75, 87, 89, 77]
    for ambig in np.uint8([82, 83, 75, 87, 89, 77]):
        ## get all site in this ambig
        idx, idy = np.where(tmpseq == ambig)
        ## get the two resolutions of the ambig
        res1, res2 = AMBIGS[ambig.view("S1")]
        ## randomly sample half those sites
        halfmask = np.random.choice([True, False], idx.shape[0])
        ## replace ambig bases with their resolutions
        for i in xrange(halfmask.shape[0]):
            if halfmask[i]:
                tmpseq[idx[i], idy[i]] = np.array(res1).view(np.uint8)
            else:
                tmpseq[idx[i], idy[i]] = np.array(res2).view(np.uint8)
    return tmpseq