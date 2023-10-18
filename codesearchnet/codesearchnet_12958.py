def chunk_to_matrices(narr, mapcol, nmask):
    """ 
    numba compiled code to get matrix fast.
    arr is a 4 x N seq matrix converted to np.int8
    I convert the numbers for ATGC into their respective index for the MAT
    matrix, and leave all others as high numbers, i.e., -==45, N==78. 
    """

    ## get seq alignment and create an empty array for filling
    mats = np.zeros((3, 16, 16), dtype=np.uint32)

    ## replace ints with small ints that index their place in the 
    ## 16x16. This no longer checks for big ints to exclude, so resolve=True
    ## is now the default, TODO. 
    last_loc = -1
    for idx in xrange(mapcol.shape[0]):
        if not nmask[idx]:
            if not mapcol[idx] == last_loc:
                i = narr[:, idx]
                mats[0, (4*i[0])+i[1], (4*i[2])+i[3]] += 1      
                last_loc = mapcol[idx]

    ## fill the alternates
    x = np.uint8(0)
    for y in np.array([0, 4, 8, 12], dtype=np.uint8):
        for z in np.array([0, 4, 8, 12], dtype=np.uint8):
            mats[1, y:y+np.uint8(4), z:z+np.uint8(4)] = mats[0, x].reshape(4, 4)
            mats[2, y:y+np.uint8(4), z:z+np.uint8(4)] = mats[0, x].reshape(4, 4).T
            x += np.uint8(1)

    return mats