def kernel_gaussian(size=100, sigma=None, forwardOnly=False):
    """
    return a 1d gassuan array of a given size and sigma.
    If sigma isn't given, it will be 1/10 of the size, which is usually good.
    """
    if sigma is None:sigma=size/10
    points=np.exp(-np.power(np.arange(size)-size/2,2)/(2*np.power(sigma,2)))
    if forwardOnly:
        points[:int(len(points)/2)]=0
    return points/sum(points)