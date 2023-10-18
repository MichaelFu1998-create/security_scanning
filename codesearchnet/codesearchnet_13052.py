def basecaller(arrayed, mindepth_majrule, mindepth_statistical, estH, estE):
    """
    call all sites in a locus array.
    """

    ## an array to fill with consensus site calls
    cons = np.zeros(arrayed.shape[1], dtype=np.uint8)
    cons.fill(78)
    arr = arrayed.view(np.uint8)
    
    ## iterate over columns
    for col in xrange(arr.shape[1]):
        ## the site of focus
        carr = arr[:, col]
        
        ## make mask of N and - sites
        mask = carr == 45
        mask += carr == 78        
        marr = carr[~mask]
        
        ## skip if only empties (e.g., N-)
        if not marr.shape[0]:
            cons[col] = 78
        
        ## skip if not variable
        elif np.all(marr == marr[0]):
            cons[col] = marr[0]
        
        ## estimate variable site call
        else:
            ## get allele freqs (first-most, second, third = p, q, r)
            counts = np.bincount(marr)
            
            pbase = np.argmax(counts)
            nump = counts[pbase]
            counts[pbase] = 0

            qbase = np.argmax(counts)
            numq = counts[qbase]
            counts[qbase] = 0

            rbase = np.argmax(counts)
            numr = counts[rbase]
            
            ## based on biallelic depth
            bidepth = nump + numq 
            if bidepth < mindepth_majrule:
                cons[col] = 78
            
            else:
                ## if depth is too high, reduce to sampled int
                if bidepth > 500:
                    base1 = int(500 * (nump / float(bidepth)))
                    base2 = int(500 * (numq / float(bidepth)))
                else:
                    base1 = nump
                    base2 = numq

                ## make statistical base call  
                if bidepth >= mindepth_statistical:
                    ishet, prob = get_binom(base1, base2, estE, estH)
                    #LOGGER.info("ishet, prob, b1, b2: %s %s %s %s", ishet, prob, base1, base2)
                    if prob < 0.95:
                        cons[col] = 78
                    else:
                        if ishet:
                            cons[col] = TRANS[(pbase, qbase)]
                        else:
                            cons[col] = pbase
                
                ## make majrule base call
                else: #if bidepth >= mindepth_majrule:
                    if nump == numq:
                        cons[col] = TRANS[(pbase, qbase)]
                    else:
                        cons[col] = pbase
    return cons.view("S1")