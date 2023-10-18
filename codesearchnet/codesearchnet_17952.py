def j2(x):
    """ A fast j2 defined in terms of other special functions """
    to_return = 2./(x+1e-15)*j1(x) - j0(x)
    to_return[x==0] = 0
    return to_return