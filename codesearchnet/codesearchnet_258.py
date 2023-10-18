def adjust_contrast_sigmoid(arr, gain, cutoff):
    """
    Adjust contrast by scaling each pixel value to ``255 * 1/(1 + exp(gain*(cutoff - I_ij/255)))``.

    dtype support::

        * ``uint8``: yes; fully tested (1) (2) (3)
        * ``uint16``: yes; tested (2) (3)
        * ``uint32``: yes; tested (2) (3)
        * ``uint64``: yes; tested (2) (3) (4)
        * ``int8``: limited; tested (2) (3) (5)
        * ``int16``: limited; tested (2) (3) (5)
        * ``int32``: limited; tested (2) (3) (5)
        * ``int64``: limited; tested (2) (3) (4) (5)
        * ``float16``: limited; tested (5)
        * ``float32``: limited; tested (5)
        * ``float64``: limited; tested (5)
        * ``float128``: no (6)
        * ``bool``: no (7)

        - (1) Handled by ``cv2``. Other dtypes are handled by ``skimage``.
        - (2) Normalization is done as ``I_ij/max``, where ``max`` is the maximum value of the
              dtype, e.g. 255 for ``uint8``. The normalization is reversed afterwards,
              e.g. ``result*255`` for ``uint8``.
        - (3) Integer-like values are not rounded after applying the contrast adjustment equation
              (before inverting the normalization to 0.0-1.0 space), i.e. projection from continuous
              space to discrete happens according to floor function.
        - (4) Note that scikit-image doc says that integers are converted to ``float64`` values before
              applying the contrast normalization method. This might lead to inaccuracies for large
              64bit integer values. Tests showed no indication of that happening though.
        - (5) Must not contain negative values. Values >=0 are fully supported.
        - (6) Leads to error in scikit-image.
        - (7) Does not make sense for contrast adjustments.

    Parameters
    ----------
    arr : numpy.ndarray
        Array for which to adjust the contrast. Dtype ``uint8`` is fastest.

    gain : number
        Multiplier for the sigmoid function's output.
        Higher values lead to quicker changes from dark to light pixels.

    cutoff : number
        Cutoff that shifts the sigmoid function in horizontal direction.
        Higher values mean that the switch from dark to light pixels happens later, i.e.
        the pixels will remain darker.

    Returns
    -------
    numpy.ndarray
        Array with adjusted contrast.

    """
    # int8 is also possible according to docs
    # https://docs.opencv.org/3.0-beta/modules/core/doc/operations_on_arrays.html#cv2.LUT , but here it seemed
    # like `d` was 0 for CV_8S, causing that to fail
    if arr.dtype.name == "uint8":
        min_value, _center_value, max_value = iadt.get_value_range_of_dtype(arr.dtype)
        dynamic_range = max_value - min_value

        value_range = np.linspace(0, 1.0, num=dynamic_range+1, dtype=np.float32)
        # 255 * 1/(1 + exp(gain*(cutoff - I_ij/255)))
        # using np.float32(.) here still works when the input is a numpy array of size 1
        gain = np.float32(gain)
        cutoff = np.float32(cutoff)
        table = min_value + dynamic_range * 1/(1 + np.exp(gain * (cutoff - value_range)))
        arr_aug = cv2.LUT(arr, np.clip(table, min_value, max_value).astype(arr.dtype))
        if arr.ndim == 3 and arr_aug.ndim == 2:
            return arr_aug[..., np.newaxis]
        return arr_aug
    else:
        return ski_exposure.adjust_sigmoid(arr, cutoff=cutoff, gain=gain)