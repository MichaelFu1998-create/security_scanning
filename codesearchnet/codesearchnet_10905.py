def wrap_periodic(a, a1, a2):
    """Folds all the values of `a` outside [a1..a2] inside that interval.
    This function is used to apply periodic boundary conditions.
    """
    a -= a1
    wrapped = np.mod(a, a2 - a1) + a1
    return wrapped