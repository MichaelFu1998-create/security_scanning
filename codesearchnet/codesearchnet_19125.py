def tsallis(alphas, Ks, dim, required, clamp=True, to_self=False):
    r'''
    Estimate the Tsallis-alpha divergence between distributions, based on kNN
    distances:  (\int p^alpha q^(1-\alpha) - 1) / (\alpha - 1)

    If clamp (the default), enforces the estimate is nonnegative.

    Returns an array of shape (num_alphas, num_Ks).
    '''
    alphas = np.reshape(alphas, (-1, 1))
    alpha_est = required

    est = alpha_est - 1
    est /= alphas - 1
    if clamp:
        np.maximum(est, 0, out=est)
    return est