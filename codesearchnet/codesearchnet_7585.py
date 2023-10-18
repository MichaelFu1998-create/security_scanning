def music(X, IP, NSIG=None, NFFT=default_NFFT, threshold=None, criteria='aic',
        verbose=False):
    """Eigen value pseudo spectrum estimate. See :func:`eigenfre`"""
    return eigen(X, IP, NSIG=NSIG, method='music', NFFT=NFFT,
                 threshold=threshold, criteria=criteria, verbose=verbose)