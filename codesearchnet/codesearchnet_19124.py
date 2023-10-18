def renyi(alphas, Ks, dim, required, min_val=np.spacing(1),
          clamp=True, to_self=False):
    r'''
    Estimate the Renyi-alpha divergence between distributions, based on kNN
    distances:  1/(\alpha-1) \log \int p^alpha q^(1-\alpha)

    If the inner integral is less than min_val (default ``np.spacing(1)``),
    uses the log of min_val instead.

    If clamp (the default), enforces that the estimates are nonnegative by
    replacing any negative estimates with 0.

    Returns an array of shape (num_alphas, num_Ks).
    '''
    alphas = np.reshape(alphas, (-1, 1))
    est = required

    est = np.maximum(est, min_val)  # TODO: can we modify in-place?
    np.log(est, out=est)
    est /= alphas - 1
    if clamp:
        np.maximum(est, 0, out=est)
    return est