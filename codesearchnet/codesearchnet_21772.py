def rfunc(a, rfunc=None, rep=0.75, **kwargs):
    """Applies func on a if a comes with a representativity coefficient rep,
    i.e. ma.count(a)/ma.size(a)>=rep. If not, returns a masked array
    """
    if float(ma.count(a)) / ma.size(a) < rep:
        return ma.masked
    else:
        if rfunc is None:
            return a
        return rfunc(a, **kwargs)