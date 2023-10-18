def as_integer_type(ary):
    '''
    Returns argument as an integer array, converting floats if convertable.
    Raises ValueError if it's a float array with nonintegral values.
    '''
    ary = np.asanyarray(ary)
    if is_integer_type(ary):
        return ary
    rounded = np.rint(ary)
    if np.any(rounded != ary):
        raise ValueError("argument array must contain only integers")
    return rounded.astype(int)