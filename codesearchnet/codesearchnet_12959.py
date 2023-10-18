def calculate(seqnon, mapcol, nmask, tests):
    """ groups together several numba compiled funcs """

    ## create empty matrices
    #LOGGER.info("tests[0] %s", tests[0])
    #LOGGER.info('seqnon[[tests[0]]] %s', seqnon[[tests[0]]])
    mats = chunk_to_matrices(seqnon, mapcol, nmask)

    ## empty svdscores for each arrangement of seqchunk
    svds = np.zeros((3, 16), dtype=np.float64)
    qscores = np.zeros(3, dtype=np.float64)
    ranks = np.zeros(3, dtype=np.float64)

    for test in range(3):
        ## get svd scores
        svds[test] = np.linalg.svd(mats[test].astype(np.float64))[1]
        ranks[test] = np.linalg.matrix_rank(mats[test].astype(np.float64))

    ## get minrank, or 11
    minrank = int(min(11, ranks.min()))
    for test in range(3):
        qscores[test] = np.sqrt(np.sum(svds[test, minrank:]**2))

    ## sort to find the best qorder
    best = np.where(qscores == qscores.min())[0]
    #best = qscores[qscores == qscores.min()][0]
    bidx = tests[best][0]
    qsnps = count_snps(mats[best][0])

    return bidx, qsnps