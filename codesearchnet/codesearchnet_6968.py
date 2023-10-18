def fire_mixing(ys=None, FLs=None):  # pragma: no cover
    '''
    Crowl, Daniel A., and Joseph F. Louvar. Chemical Process Safety:
    Fundamentals with Applications. 2E. Upper Saddle River, N.J:
    Prentice Hall, 2001.


    >>> fire_mixing(ys=normalize([0.0024, 0.0061, 0.0015]), FLs=[.012, .053, .031])
    0.02751172136637643
    >>> fire_mixing(ys=normalize([0.0024, 0.0061, 0.0015]), FLs=[.075, .15, .32])
    0.12927551844869378
    '''
    return 1./sum([yi/FLi for yi, FLi in zip(ys, FLs)])