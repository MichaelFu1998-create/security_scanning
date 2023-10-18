def hellinger(Ks, dim, required, clamp=True, to_self=False):
    r'''
    Estimate the Hellinger distance between distributions, based on kNN
    distances:  \sqrt{1 - \int \sqrt{p q}}

    Always enforces 0 <= H, to be able to sqrt; if clamp, also enforces
    H <= 1.

    Returns a vector: one element for each K.
    '''
    bc = required
    est = 1 - bc
    np.maximum(est, 0, out=est)
    if clamp:
        np.minimum(est, 1, out=est)
    np.sqrt(est, out=est)
    return est