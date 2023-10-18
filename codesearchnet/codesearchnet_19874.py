def getAvgBySweep(abf,feature,T0=None,T1=None):
    """return average of a feature divided by sweep."""
    if T1 is None:
        T1=abf.sweepLength
    if T0 is None:
        T0=0
    data = [np.empty((0))]*abf.sweeps
    for AP in cm.dictFlat(cm.matrixToDicts(abf.APs)):
        if T0<AP['sweepT']<T1:
            val=AP[feature]
            data[int(AP['sweep'])]=np.concatenate((data[int(AP['sweep'])],[val]))
    for sweep in range(abf.sweeps):
        if len(data[sweep])>1 and np.any(data[sweep]):
            data[sweep]=np.nanmean(data[sweep])
        elif len(data[sweep])==1:
            data[sweep]=data[sweep][0]
        else:
            data[sweep]=np.nan
    return data