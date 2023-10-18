def filter_indels(data, superints, edgearr):
    """
    Filter max indels. Needs to split to apply to each read separately.
    The dimensions of superseqs are (chunk, sum(sidx), maxlen).
    """

    maxinds = np.array(data.paramsdict["max_Indels_locus"]).astype(np.int64)

    ## an empty array to fill with failed loci
    ifilter = np.zeros(superints.shape[0], dtype=np.bool_)

    ## if paired then worry about splits
    if "pair" in data.paramsdict["datatype"]:
        for idx in xrange(superints.shape[0]):
            block1 = superints[idx, :, edgearr[idx, 0]:edgearr[idx, 1]]
            block2 = superints[idx, :, edgearr[idx, 2]:edgearr[idx, 3]]

            sums1 = maxind_numba(block1)
            ## If all loci are merged then block2 will be empty which will
            ## cause maxind_numba to throw a very confusing ValueError
            if np.any(block2):
                sums2 = maxind_numba(block2)
            else:
                sums2 = 0

            if (sums1 > maxinds[0]) or (sums2 > maxinds[1]):
                ifilter[idx] = True

    else:
        for idx in xrange(superints.shape[0]):
            ## get block based on edge filters
            block = superints[idx, :, edgearr[idx, 0]:edgearr[idx, 1]]
            ## shorten block to exclude terminal indels
            ## if data at this locus (not already filtered by edges/minsamp)
            if block.shape[1] > 1:
                try:
                    sums = maxind_numba(block)
                except ValueError as inst:
                    msg = "All loci filterd by max_Indels_locus. Try increasing this parameter value."
                    raise IPyradError(msg)
                except Exception as inst:
                    LOGGER.error("error in block {}".format(block))
                #LOGGER.info("maxind numba %s %s", idx, sums)
                #LOGGER.info("sums, maxinds[0], compare: %s %s %s",
                #             sums, maxinds[0], sums > maxinds[0])
                if sums > maxinds[0]:
                    ifilter[idx] = True

    LOGGER.info("--------------maxIndels sums %s", ifilter.sum())
    return ifilter