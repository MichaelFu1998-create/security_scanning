def filter_minsamp(data, superints):
    """
    Filter minimum # of samples per locus from superseqs[chunk]. The shape
    of superseqs is [chunk, sum(sidx), maxlen]
    """
    ## global minsamp
    minsamp = data.paramsdict["min_samples_locus"]

    ## use population minsamps
    if data.populations:
        ## data._populations will look like this:
        ## {'a': (3, [0, 1, 2, 3],
        ##  'b': (3, [4, 5, 6, 7],
        ##  'c': (3, [8, 9, 10, 11]}
        LOGGER.info("POPULATIONS %s", data.populations)
        
        ## superints has already been subsampled by sidx
        ## get the sidx values for each pop
        minfilters = []
        for pop in data._populations:
            samps = data._populations[pop][1]
            minsamp = data._populations[pop][0]
            mini = np.sum(~np.all(superints[:, samps, :] == 78, axis=2), axis=1) < minsamp
            minfilters.append(mini)
        ## get sum across all pops for each locus
        minfilt = np.any(minfilters, axis=0)

    else:
        ## if not pop-file use global minsamp filter
        minfilt = np.sum(~np.all(superints == 78, axis=2), axis=1) < minsamp
        #LOGGER.info("Filtered by min_samples_locus - {}".format(minfilt.sum()))
    return minfilt