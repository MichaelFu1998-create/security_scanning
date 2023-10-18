def dictVals(l,key):
    """Return all 'key' from a list of dicts. (or list of list of dicts)"""
    dicts=dictFlat(l)
    vals=np.empty(len(dicts))*np.nan
    for i in range(len(dicts)):
        if key in dicts[i]:
            vals[i]=dicts[i][key]
    return vals