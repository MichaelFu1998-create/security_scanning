def matrixToDicts(data):
    """given a recarray, return it as a list of dicts."""

    # 1D array
    if "float" in str(type(data[0])):
        d={}
        for x in range(len(data)):
            d[data.dtype.names[x]]=data[x]
        return d

    # 2D array
    l=[]
    for y in range(len(data)):
        d={}
        for x in range(len(data[y])):
            d[data.dtype.names[x]]=data[y][x]
        l.append(d)
    return l