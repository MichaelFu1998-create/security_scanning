def dictAvg(listOfDicts,key,stdErr=False):
    """Given a list (l) of dicts (d), return AV and SD."""
    vals=dictVals(listOfDicts,key)
    if len(vals) and np.any(vals):
        av=np.nanmean(vals)
        er=np.nanstd(vals)
        if stdErr:
            er=er/np.sqrt(np.count_nonzero(~np.isnan(er)))
    else:
        av,er=np.nan,np.nan
    return av,er