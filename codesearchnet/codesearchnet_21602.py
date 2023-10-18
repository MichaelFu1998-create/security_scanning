def generic_masked(arr, attrs=None, minv=None, maxv=None, mask_nan=True):
    """
    Returns a masked array with anything outside of values masked.
    The minv and maxv parameters take precendence over any dict values.
    The valid_range attribute takes precendence over the valid_min and
    valid_max attributes.
    """
    attrs = attrs or {}

    if 'valid_min' in attrs:
        minv = safe_attribute_typing(arr.dtype, attrs['valid_min'])
    if 'valid_max' in attrs:
        maxv = safe_attribute_typing(arr.dtype, attrs['valid_max'])
    if 'valid_range' in attrs:
        vr = attrs['valid_range']
        minv = safe_attribute_typing(arr.dtype, vr[0])
        maxv = safe_attribute_typing(arr.dtype, vr[1])

    # Get the min/max of values that the hardware supports
    try:
        info = np.iinfo(arr.dtype)
    except ValueError:
        info = np.finfo(arr.dtype)

    minv = minv if minv is not None else info.min
    maxv = maxv if maxv is not None else info.max

    if mask_nan is True:
        arr = np.ma.fix_invalid(arr)

    return np.ma.masked_outside(
        arr,
        minv,
        maxv
    )