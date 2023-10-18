def snpcount_numba(superints, snpsarr):
    """
    Used to count the number of unique bases in a site for snpstring.
    """
    ## iterate over all loci
    for iloc in xrange(superints.shape[0]):
        for site in xrange(superints.shape[2]):

            ## make new array
            catg = np.zeros(4, dtype=np.int16)

            ## a list for only catgs
            ncol = superints[iloc, :, site]
            for idx in range(ncol.shape[0]):
                if ncol[idx] == 67: #C
                    catg[0] += 1
                elif ncol[idx] == 65: #A
                    catg[1] += 1
                elif ncol[idx] == 84: #T
                    catg[2] += 1
                elif ncol[idx] == 71: #G
                    catg[3] += 1
                elif ncol[idx] == 82: #R
                    catg[1] += 1        #A
                    catg[3] += 1        #G
                elif ncol[idx] == 75: #K
                    catg[2] += 1        #T
                    catg[3] += 1        #G
                elif ncol[idx] == 83: #S
                    catg[0] += 1        #C
                    catg[3] += 1        #G
                elif ncol[idx] == 89: #Y
                    catg[0] += 1        #C
                    catg[2] += 1        #T
                elif ncol[idx] == 87: #W
                    catg[1] += 1        #A
                    catg[2] += 1        #T
                elif ncol[idx] == 77: #M
                    catg[0] += 1        #C
                    catg[1] += 1        #A


            ## get second most common site
            catg.sort()
            ## if invariant e.g., [0, 0, 0, 9], then nothing (" ")
            if not catg[2]:
                pass
            else:
                if catg[2] > 1:
                    snpsarr[iloc, site, 1] = True
                else:
                    snpsarr[iloc, site, 0] = True
    return snpsarr