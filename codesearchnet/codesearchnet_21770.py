def max(a, rep=0.75, **kwargs):
    """Compute the max along a 1D array like ma.mean,
    but with a representativity coefficient : if ma.count(a)/ma.size(a)>=rep,
    then the result is a masked value
    """
    return rfunc(a, ma.max, rep, **kwargs)