def as_features(X, stack=False, bare=False):
    '''
    Returns a version of X as a :class:`Features` object.

    Parameters
    ----------
    stack : boolean, default False
        Make a stacked version of X. Note that if X is a features object,
        this will stack it in-place, since that's usually what you want.
        (If not, just use the :class:`Features` constructor instead.)

    bare : boolean, default False
        Return a bare version of X (no metadata).

    Returns
    -------
    feats : :class:`Features`
        A version of X. If X is already a :class:`Features` object, the original
        X may be returned, depending on the arguments.
    '''
    if isinstance(X, Features):
        if stack:
            X.make_stacked()
        return X.bare() if bare else X
    return Features(X, stack=stack, bare=bare)