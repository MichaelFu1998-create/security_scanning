def get_values(abf,key="freq",continuous=False):
    """returns Xs, Ys (the key), and sweep #s for every AP found."""
    Xs,Ys,Ss=[],[],[]
    for sweep in range(abf.sweeps):
        for AP in cm.matrixToDicts(abf.APs):
            if not AP["sweep"]==sweep:
                continue
            Ys.append(AP[key])
            Ss.append(AP["sweep"])
            if continuous:
                Xs.append(AP["expT"])
            else:
                Xs.append(AP["sweepT"])

    return np.array(Xs),np.array(Ys),np.array(Ss)