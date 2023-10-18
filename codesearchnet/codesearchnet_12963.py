def get_spans(maparr, spans):
    """ get span distance for each locus in original seqarray """
    ## start at 0, finds change at 1-index of map file
    bidx = 1
    spans = np.zeros((maparr[-1, 0], 2), np.uint64)
    ## read through marr and record when locus id changes
    for idx in xrange(1, maparr.shape[0]):
        cur = maparr[idx, 0]
        if cur != bidx:
            idy = idx + 1
            spans[cur-2, 1] = idx
            spans[cur-1, 0] = idx
            bidx = cur
    spans[-1, 1] = maparr[-1, -1]
    return spans