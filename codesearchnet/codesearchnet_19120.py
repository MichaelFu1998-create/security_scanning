def alpha_div(alphas, Ks, dim, num_q, rhos, nus):
    r'''
    Estimate the alpha divergence between distributions:
        \int p^\alpha q^(1-\alpha)
    based on kNN distances.

    Used in Renyi, Hellinger, Bhattacharyya, Tsallis divergences.

    Enforces that estimates are >= 0.

    Returns divergence estimates with shape (num_alphas, num_Ks).
    '''
    return _get_alpha_div(alphas, Ks, dim)(num_q, rhos, nus)