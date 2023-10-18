def _get_signal_space(S, NP, verbose=False, threshold=None, NSIG=None,
                     criteria='aic'):
    """todo


    """
    from .criteria import aic_eigen, mdl_eigen
    # This section selects automatically the noise and signal subspaces.
    # NSIG being the number of eigenvalues corresponding to signals.
    if NSIG is None:
        if threshold is None:
            logging.debug('computing NSIG using AIC method')
            # get the minimum index of the AIC vector
            if criteria == 'aic':
                aic = aic_eigen(S, NP*2)
            elif criteria == 'mdl':
                aic = mdl_eigen(S, NP*2)
            # get the minimum index of the AIC vector, add 1 to get the NSIG
            NSIG = np.argmin(aic) + 1
            logging.debug('NSIG=', NSIG, ' found as the number of pertinent sinusoids')
        else:
            logging.debug('computing NSIG using user threshold ')
            # following an idea from Matlab, pmusic, we look at the minimum
            # eigen value, and split the eigen values above and below
            # K times min eigen value, where K is >1
            m = threshold * min(S)
            new_s = S[np.where(S>m)]
            NSIG = len(new_s)
            logging.debug('found', NSIG)
            if NSIG == 0:
                NSIG = 1
    return NSIG