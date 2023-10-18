def ndist(data,Xs):
    """
    given some data and a list of X posistions, return the normal
    distribution curve as a Y point at each of those Xs.
    """
    sigma=np.sqrt(np.var(data))
    center=np.average(data)
    curve=mlab.normpdf(Xs,center,sigma)
    curve*=len(data)*HIST_RESOLUTION
    return curve