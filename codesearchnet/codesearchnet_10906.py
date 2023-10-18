def wrap_mirror(a, a1, a2):
    """Folds all the values of `a` outside [a1..a2] inside that interval.
    This function is used to apply mirror-like boundary conditions.
    """
    a[a > a2] = a2 - (a[a > a2] - a2)
    a[a < a1] = a1 + (a1 - a[a < a1])
    return a