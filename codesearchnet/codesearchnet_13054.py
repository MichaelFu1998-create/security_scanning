def nfilter4(consens, hidx, arrayed):
    """ applies max haplotypes filter returns pass and consens"""

    ## if less than two Hs then there is only one allele
    if len(hidx) < 2:
        return consens, 1

    ## store base calls for hetero sites
    harray = arrayed[:, hidx]

    ## remove any reads that have N or - base calls at hetero sites
    ## these cannot be used when calling alleles currently.
    harray = harray[~np.any(harray == "-", axis=1)]
    harray = harray[~np.any(harray == "N", axis=1)]

    ## get counts of each allele (e.g., AT:2, CG:2)
    ccx = Counter([tuple(i) for i in harray])

    ## Two possibilities we would like to distinguish, but we can't. Therefore,
    ## we just throw away low depth third alleles that are within seq. error.
    ## 1) a third base came up as a sequencing error but is not a unique allele
    ## 2) a third or more unique allele is there but at low frequency

    ## remove low freq alleles if more than 2, since they may reflect
    ## sequencing errors at hetero sites, making a third allele, or a new
    ## allelic combination that is not real.
    if len(ccx) > 2:
        totdepth = harray.shape[0]
        cutoff = max(1, totdepth // 10)
        alleles = [i for i in ccx if ccx[i] > cutoff]
    else:
        alleles = ccx.keys()

    ## how many high depth alleles?
    nalleles = len(alleles)

    ## if 2 alleles then save the phase using lowercase coding
    if nalleles == 2:
        try:
            consens = storealleles(consens, hidx, alleles)
        except (IndexError, KeyError):
            ## the H sites do not form good alleles
            LOGGER.info("failed at phasing loc, skipping")
            LOGGER.info("""
    consens %s
    hidx %s
    alleles %s
                """, consens, hidx, alleles)
        return consens, nalleles
    ## just return the info for later filtering
    else:
        return consens, nalleles