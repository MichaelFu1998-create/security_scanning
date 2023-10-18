def jensen_shannon_core(Ks, dim, num_q, rhos, nus):
    r'''
    Estimates
          1/2 mean_X( d * log radius of largest ball in X+Y around X_i
                                with no more than M/(n+m-1) weight
                                where X points have weight 1 / (2 n - 1)
                                  and Y points have weight n / (m (2 n - 1))
                      - digamma(# of neighbors in that ball))

    This is the core pairwise component of the estimator of Jensen-Shannon
    divergence based on the Hino-Murata weighted information estimator. See
    the docstring for jensen_shannon for an explanation.
    '''
    ns = np.array([rhos.shape[0], num_q])
    return _get_jensen_shannon_core(Ks, dim, ns)[0](num_q, rhos, nus)