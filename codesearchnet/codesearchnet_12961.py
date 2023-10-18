def shuffle_cols(seqarr, newarr, cols):
    """ used in bootstrap resampling without a map file """
    for idx in xrange(cols.shape[0]):
        newarr[:, idx] = seqarr[:, cols[idx]]
    return newarr