def adjust_contrast_linear(arr, alpha):
    """Adjust contrast by scaling each pixel value to ``127 + alpha*(I_ij-127)``.

    dtype support::

        * ``uint8``: yes; fully tested (1) (2)
        * ``uint16``: yes; tested (2)
        * ``uint32``: yes; tested (2)
        * ``uint64``: no (3)
        * ``int8``: yes; tested (2)
        * ``int16``: yes; tested (2)
        * ``int32``: yes; tested (2)
        * ``int64``: no (2)
        * ``float16``: yes; tested (2)
        * ``float32``: yes; tested (2)
        * ``float64``: yes; tested (2)
        * ``float128``: no (2)
        * ``bool``: no (4)

        - (1) Handled by ``cv2``. Other dtypes are handled by raw ``numpy``.
        - (2) Only tested for reasonable alphas with up to a value of around 100.
        - (3) Conversion to ``float64`` is done during augmentation, hence ``uint64``, ``int64``,
              and ``float128`` support cannot be guaranteed.
        - (4) Does not make sense for contrast adjustments.

    Parameters
    ----------
    arr : numpy.ndarray
        Array for which to adjust the contrast. Dtype ``uint8`` is fastest.

    alpha : number
        Multiplier to linearly pronounce (>1.0), dampen (0.0 to 1.0) or invert (<0.0) the
        difference between each pixel value and the center value, e.g. ``127`` for ``uint8``.

    Returns
    -------
    numpy.ndarray
        Array with adjusted contrast.

    """
    # int8 is also possible according to docs
    # https://docs.opencv.org/3.0-beta/modules/core/doc/operations_on_arrays.html#cv2.LUT , but here it seemed
    # like `d` was 0 for CV_8S, causing that to fail
    if arr.dtype.name == "uint8":
        min_value, center_value, max_value = iadt.get_value_range_of_dtype(arr.dtype)

        value_range = np.arange(0, 256, dtype=np.float32)
        # 127 + alpha*(I_ij-127)
        # using np.float32(.) here still works when the input is a numpy array of size 1
        alpha = np.float32(alpha)
        table = center_value + alpha * (value_range - center_value)
        arr_aug = cv2.LUT(arr, np.clip(table, min_value, max_value).astype(arr.dtype))
        if arr.ndim == 3 and arr_aug.ndim == 2:
            return arr_aug[..., np.newaxis]
        return arr_aug
    else:
        input_dtype = arr.dtype
        _min_value, center_value, _max_value = iadt.get_value_range_of_dtype(input_dtype)
        if input_dtype.kind in ["u", "i"]:
            center_value = int(center_value)
        image_aug = center_value + alpha * (arr.astype(np.float64)-center_value)
        image_aug = iadt.restore_dtypes_(image_aug, input_dtype)
        return image_aug