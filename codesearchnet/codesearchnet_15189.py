def _bstar_1effect(beta, alpha, yTBy, yTBX, yTBM, XTBX, XTBM, MTBM):
    """
    Same as :func:`_bstar_set` but for single-effect.
    """
    from numpy_sugar import epsilon
    from numpy_sugar.linalg import dotd
    from numpy import sum

    r = full(MTBM[0].shape[0], yTBy)
    r -= 2 * add.reduce([dot(i, beta) for i in yTBX])
    r -= 2 * add.reduce([i * alpha for i in yTBM])
    r += add.reduce([dotd(beta.T, dot(i, beta)) for i in XTBX])
    r += add.reduce([dotd(beta.T, i * alpha) for i in XTBM])
    r += add.reduce([sum(alpha * i * beta, axis=0) for i in XTBM])
    r += add.reduce([alpha * i.ravel() * alpha for i in MTBM])
    return clip(r, epsilon.tiny, inf)