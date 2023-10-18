def quietParts(data,percentile=10):
    """
    Given some data (Y) break it into chunks and return just the quiet ones.
    Returns data where the variance for its chunk size is below the given percentile.
    CHUNK_POINTS should be adjusted so it's about 10ms of data.
    """
    nChunks=int(len(Y)/CHUNK_POINTS)
    chunks=np.reshape(Y[:nChunks*CHUNK_POINTS],(nChunks,CHUNK_POINTS))
    variances=np.var(chunks,axis=1)
    percentiles=np.empty(len(variances))
    for i,variance in enumerate(variances):
        percentiles[i]=sorted(variances).index(variance)/len(variances)*100
    selected=chunks[np.where(percentiles<=percentile)[0]].flatten()
    return selected