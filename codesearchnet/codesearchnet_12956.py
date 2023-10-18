def count_snps(mat):
    """ 
    get dstats from the count array and return as a float tuple 
    """

    ## get [aabb, baba, abba, aaab] 
    snps = np.zeros(4, dtype=np.uint32)

    ## get concordant (aabb) pis sites
    snps[0] = np.uint32(\
           mat[0, 5] + mat[0, 10] + mat[0, 15] + \
           mat[5, 0] + mat[5, 10] + mat[5, 15] + \
           mat[10, 0] + mat[10, 5] + mat[10, 15] + \
           mat[15, 0] + mat[15, 5] + mat[15, 10])

    ## get discordant (baba) sites
    for i in range(16):
        if i % 5:
            snps[1] += mat[i, i]
    
    ## get discordant (abba) sites
    snps[2] = mat[1, 4] + mat[2, 8] + mat[3, 12] +\
              mat[4, 1] + mat[6, 9] + mat[7, 13] +\
              mat[8, 2] + mat[9, 6] + mat[11, 14] +\
              mat[12, 3] + mat[13, 7] + mat[14, 11]

    ## get autapomorphy sites
    snps[3] = (mat.sum() - np.diag(mat).sum()) - snps[2]

    return snps