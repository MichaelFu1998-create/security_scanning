def filter_maxsnp(data, superints, edgearr):
    """
    Filter max # of SNPs per locus. Do R1 and R2 separately if PE.
    Also generate the snpsite line for the .loci format and save in the snp arr
    This uses the edge filters that have been built based on trimming, and
    saves the snps array with edges filtered. **Loci are not yet filtered.**
    """

    ## an empty array to count with failed loci
    snpfilt = np.zeros(superints.shape[0], dtype=np.bool)
    snpsarr = np.zeros((superints.shape[0], superints.shape[2], 2), dtype=np.bool)
    maxsnps = np.array(data.paramsdict['max_SNPs_locus'], dtype=np.int16)

    ## get the per site snp string | shape=(chunk, maxlen)
    # snpsarr[:, :, 0] = snps == "-"
    # snpsarr[:, :, 1] = snps == "*"
    snpsarr = snpcount_numba(superints, snpsarr)
    LOGGER.info("---found the snps: %s", snpsarr.sum())
    snpfilt, snpsarr = snpfilter_numba(snpsarr, snpfilt, edgearr, maxsnps)
    LOGGER.info("---filtered snps: %s", snpfilt.sum())
    return snpfilt, snpsarr