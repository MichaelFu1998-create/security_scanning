def pole_removal(noise, poles=None, sig=3):
    """
    Remove the noise poles from a 2d noise distribution to show that affects
    the real-space noise picture.  
    
    noise -- fftshifted 2d array of q values

    poles -- N,2 list of pole locations. the last index is in the order y,x as
    determined by mpl interactive plots

    for example: poles = np.array([[190,277], [227,253], [233, 256]]
    """
    center = np.array(noise.shape)/2

    v = np.rollaxis(
            np.array(
                np.meshgrid(*(np.arange(s) for s in noise.shape), indexing='ij')
            ), 0, 3
        ).astype("float")
    filter = np.zeros_like(noise, dtype='float')

    for p in poles:
        for pp in [p, center - (p-center)]:
            dist = ((v-pp)**2).sum(axis=-1)
            filter += np.exp(-dist / (2*sig**2))

    filter[filter > 1] = 1
    return noise*(1-filter)