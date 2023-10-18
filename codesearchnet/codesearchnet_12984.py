def select_samples(dbsamples, samples, pidx=None):
    """
    Get the row index of samples that are included. If samples are in the
    'excluded' they were already filtered out of 'samples' during _get_samples.
    """
    ## get index from dbsamples
    samples = [i.name for i in samples]
    if pidx:
        sidx = [list(dbsamples[pidx]).index(i) for i in samples]
    else:
        sidx = [list(dbsamples).index(i) for i in samples]
    sidx.sort()
    return sidx