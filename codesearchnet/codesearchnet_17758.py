def split_list(l,N):
    '''
    Subdivide list into N lists
    '''
    npmode = isinstance(l,np.ndarray)
    if npmode:
        l=list(l)
    g=np.concatenate((np.array([0]),np.cumsum(split_integer(len(l),length=N))))
    s=[l[g[i]:g[i+1]] for i in range(N)]
    if npmode:
        s=[np.array(sl) for sl in s]
    return s