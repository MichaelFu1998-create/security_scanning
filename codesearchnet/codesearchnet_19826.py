def matrixfromDicts(dicts):
    """
    Give a list of dicts (or list of list of dicts) return a structured array.
    Headings will be sorted in alphabetical order.
    """
    if 'numpy' in str(type(dicts)):
        return dicts #already an array?
    names=set([])
    dicts=dictFlat(dicts)
    for item in dicts:
        names=names.union(list(item.keys()))
    names=sorted(list(names))
    data=np.empty((len(dicts),len(names)),dtype=float)*np.nan
    for y in range(len(dicts)):
        for key in dicts[y].keys():
            for x in range(len(names)):
                if names[x] in dicts[y]:
                    data[y,x]=dicts[y][names[x]]
    if len(dicts):
        data=np.core.records.fromarrays(data.transpose(),names=names)
    return data