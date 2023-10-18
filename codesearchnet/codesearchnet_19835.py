def numpyAlignXY(data):
    """
    given a numpy array (XYXYXY columns), return it aligned.
    data returned will be XYYY. NANs may be returned.
    """
    print(data)
    Xs=data.flatten()[::2] # get all X values
    Xs=Xs[~np.isnan(Xs)] # remove nans
    Xs=sorted(list(set(Xs))) # eliminate duplicates then sort it
    aligned=np.empty((len(Xs),int(len(data[0])/2+1)))*np.nan
    aligned[:,0]=Xs
    for col in range(0,len(data[0]),2):
        for row in range(len(data)):
            X=data[row,col]
            Y=data[row,col+1]
            if np.isnan(X) or np.isnan(Y):
                continue
            aligned[Xs.index(X),int(col/2+1)]=Y
    return aligned