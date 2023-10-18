def bhattacharyya(Ks, dim, required, clamp=True, to_self=False):
    r'''
    Estimate the Bhattacharyya coefficient between distributions, based on kNN
    distances:  \int \sqrt{p q}

    If clamp (the default), enforces 0 <= BC <= 1.

    Returns an array of shape (num_Ks,).
    '''
    est = required
    if clamp:
        est = np.minimum(est, 1)  # BC <= 1
    return est