def _loci_to_arr(loci, taxdict, mindict):
    """
    return a frequency array from a loci file for all loci with taxa from 
    taxdict and min coverage from mindict. 
    """

    ## make the array (4 or 5) and a mask array to remove loci without cov
    nloci = len(loci)
    maxlen = np.max(np.array([len(locus.split("\n")[0]) for locus in loci]))
    keep = np.zeros(nloci, dtype=np.bool_)
    arr = np.zeros((nloci, 4, maxlen), dtype=np.float64)

    ## six rows b/c one for each p3, and for the fused p3 ancestor
    if len(taxdict) == 5:
        arr = np.zeros((nloci, 6, maxlen), dtype=np.float64)

    ## if not mindict, make one that requires 1 in each taxon
    if isinstance(mindict, int):
        mindict = {i: mindict for i in taxdict}
    elif isinstance(mindict, dict):
        mindict = {i: mindict[i] for i in taxdict}
    else:
        mindict = {i: 1 for i in taxdict}

    ## raise error if names are not 'p[int]' 
    allowed_names = ['p1', 'p2', 'p3', 'p4', 'p5']
    if any([i not in allowed_names for i in taxdict]):
        raise IPyradError(\
            "keys in taxdict must be named 'p1' through 'p4' or 'p5'")

    ## parse key names
    keys = sorted([i for i in taxdict.keys() if i[0] == 'p'])
    outg = keys[-1]

    ## grab seqs just for the good guys
    for loc in xrange(nloci):

        ## parse the locus
        lines = loci[loc].split("\n")[:-1]
        names = [i.split()[0] for i in lines]
        seqs = np.array([list(i.split()[1]) for i in lines])

        ## check that names cover the taxdict (still need to check by site)
        covs = [sum([j in names for j in taxdict[tax]]) >= mindict[tax] \
                for tax in taxdict]

        ## keep locus
        if all(covs):
            keep[loc] = True

            ## get the refseq
            refidx = np.where([i in taxdict[outg] for i in names])[0]
            refseq = seqs[refidx].view(np.uint8)
            ancestral = np.array([reftrick(refseq, GETCONS2)[:, 0]])

            ## freq of ref in outgroup
            iseq = _reffreq2(ancestral, refseq, GETCONS2)
            arr[loc, -1, :iseq.shape[1]] = iseq 

            ## enter 4-taxon freqs
            if len(taxdict) == 4:
                for tidx, key in enumerate(keys[:-1]):

                    ## get idx of names in test tax
                    nidx = np.where([i in taxdict[key] for i in names])[0]
                    sidx = seqs[nidx].view(np.uint8)
                   
                    ## get freq of sidx
                    iseq = _reffreq2(ancestral, sidx, GETCONS2)
                   
                    ## fill it in 
                    arr[loc, tidx, :iseq.shape[1]] = iseq

            else:

                ## entere p5; and fill it in
                iseq = _reffreq2(ancestral, refseq, GETCONS2) 
                arr[loc, -1, :iseq.shape[1]] = iseq 
                
                ## enter p1
                nidx = np.where([i in taxdict['p1'] for i in names])[0]
                sidx = seqs[nidx].view(np.uint8)
                iseq = _reffreq2(ancestral, sidx, GETCONS2)
                arr[loc, 0, :iseq.shape[1]] = iseq
                
                ## enter p2
                nidx = np.where([i in taxdict['p2'] for i in names])[0]
                sidx = seqs[nidx].view(np.uint8)
                iseq = _reffreq2(ancestral, sidx, GETCONS2)
                arr[loc, 1, :iseq.shape[1]] = iseq
                
                ## enter p3 with p4 masked, and p4 with p3 masked
                nidx = np.where([i in taxdict['p3'] for i in names])[0]
                nidy = np.where([i in taxdict['p4'] for i in names])[0]
                sidx = seqs[nidx].view(np.uint8)
                sidy = seqs[nidy].view(np.uint8)
                xseq = _reffreq2(ancestral, sidx, GETCONS2)
                yseq = _reffreq2(ancestral, sidy, GETCONS2)
                mask3 = xseq != 0
                mask4 = yseq != 0
                xseq[mask4] = 0
                yseq[mask3] = 0
                arr[loc, 2, :xseq.shape[1]] = xseq
                arr[loc, 3, :yseq.shape[1]] = yseq
                
                ## enter p34 
                nidx = nidx.tolist() + nidy.tolist()
                sidx = seqs[nidx].view(np.uint8)
                iseq = _reffreq2(ancestral, sidx, GETCONS2)
                arr[loc, 4, :iseq.shape[1]] = iseq


    ## size-down array to the number of loci that have taxa for the test
    arr = arr[keep, :, :]

    ## size-down sites to 
    arr = masknulls(arr)

    return arr, keep