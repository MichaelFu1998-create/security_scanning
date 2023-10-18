def get_shape(spans, loci):
    """ get shape of new bootstrap resampled locus array """
    width = 0
    for idx in xrange(loci.shape[0]):
        width += spans[loci[idx], 1] - spans[loci[idx], 0]
    return width