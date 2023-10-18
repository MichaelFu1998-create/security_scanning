def _log_prior_transit(theta, priorbounds):
    '''
    Assume priors on all parameters have uniform probability.
    '''
    # priorbounds contains the input priors, and because of how we previously
    # sorted theta, its sorted keys tell us which parts of theta correspond to
    # which physical quantities.

    allowed = True
    for ix, key in enumerate(np.sort(list(priorbounds.keys()))):
        if priorbounds[key][0] < theta[ix] < priorbounds[key][1]:
            allowed = True and allowed
        else:
            allowed = False

    if allowed:
        return 0.

    return -np.inf