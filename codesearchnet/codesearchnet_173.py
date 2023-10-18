def imresize_many_images(images, sizes=None, interpolation=None):
    """
    Resize many images to a specified size.

    dtype support::

        * ``uint8``: yes; fully tested
        * ``uint16``: yes; tested
        * ``uint32``: no (1)
        * ``uint64``: no (2)
        * ``int8``: yes; tested (3)
        * ``int16``: yes; tested
        * ``int32``: limited; tested (4)
        * ``int64``: no (2)
        * ``float16``: yes; tested (5)
        * ``float32``: yes; tested
        * ``float64``: yes; tested
        * ``float128``: no (1)
        * ``bool``: yes; tested (6)

        - (1) rejected by ``cv2.imresize``
        - (2) results too inaccurate
        - (3) mapped internally to ``int16`` when interpolation!="nearest"
        - (4) only supported for interpolation="nearest", other interpolations lead to cv2 error
        - (5) mapped internally to ``float32``
        - (6) mapped internally to ``uint8``

    Parameters
    ----------
    images : (N,H,W,[C]) ndarray or list of (H,W,[C]) ndarray
        Array of the images to resize.
        Usually recommended to be of dtype uint8.

    sizes : float or iterable of int or iterable of float
        The new size of the images, given either as a fraction (a single float) or as
        a ``(height, width)`` tuple of two integers or as a ``(height fraction, width fraction)``
        tuple of two floats.

    interpolation : None or str or int, optional
        The interpolation to use during resize.
        If int, then expected to be one of:

            * ``cv2.INTER_NEAREST`` (nearest neighbour interpolation)
            * ``cv2.INTER_LINEAR`` (linear interpolation)
            * ``cv2.INTER_AREA`` (area interpolation)
            * ``cv2.INTER_CUBIC`` (cubic interpolation)

        If string, then expected to be one of:

            * ``nearest`` (identical to ``cv2.INTER_NEAREST``)
            * ``linear`` (identical to ``cv2.INTER_LINEAR``)
            * ``area`` (identical to ``cv2.INTER_AREA``)
            * ``cubic`` (identical to ``cv2.INTER_CUBIC``)

        If None, the interpolation will be chosen automatically. For size
        increases, area interpolation will be picked and for size decreases,
        linear interpolation will be picked.

    Returns
    -------
    result : (N,H',W',[C]) ndarray
        Array of the resized images.

    Examples
    --------
    >>> imresize_many_images(np.zeros((2, 16, 16, 3), dtype=np.uint8), 2.0)

    Converts 2 RGB images of height and width 16 to images of height and width 16*2 = 32.

    >>> imresize_many_images(np.zeros((2, 16, 16, 3), dtype=np.uint8), (16, 32))

    Converts 2 RGB images of height and width 16 to images of height 16 and width 32.

    >>> imresize_many_images(np.zeros((2, 16, 16, 3), dtype=np.uint8), (2.0, 4.0))

    Converts 2 RGB images of height and width 16 to images of height 32 and width 64.

    """
    # we just do nothing if the input contains zero images
    # one could also argue that an exception would be appropriate here
    if len(images) == 0:
        return images

    # verify that all input images have height/width > 0
    do_assert(
        all([image.shape[0] > 0 and image.shape[1] > 0 for image in images]),
        ("Cannot resize images, because at least one image has a height and/or width of zero. "
         + "Observed shapes were: %s.") % (str([image.shape for image in images]),)
    )

    # verify that sizes contains only values >0
    if is_single_number(sizes) and sizes <= 0:
        raise Exception(
            "Cannot resize to the target size %.8f, because the value is zero or lower than zero." % (sizes,))
    elif isinstance(sizes, tuple) and (sizes[0] <= 0 or sizes[1] <= 0):
        sizes_str = [
            "int %d" % (sizes[0],) if is_single_integer(sizes[0]) else "float %.8f" % (sizes[0],),
            "int %d" % (sizes[1],) if is_single_integer(sizes[1]) else "float %.8f" % (sizes[1],),
        ]
        sizes_str = "(%s, %s)" % (sizes_str[0], sizes_str[1])
        raise Exception(
            "Cannot resize to the target sizes %s. At least one value is zero or lower than zero." % (sizes_str,))

    # change after the validation to make the above error messages match the original input
    if is_single_number(sizes):
        sizes = (sizes, sizes)
    else:
        do_assert(len(sizes) == 2, "Expected tuple with exactly two entries, got %d entries." % (len(sizes),))
        do_assert(all([is_single_number(val) for val in sizes]),
                  "Expected tuple with two ints or floats, got types %s." % (str([type(val) for val in sizes]),))

    # if input is a list, call this function N times for N images
    # but check beforehand if all images have the same shape, then just convert to a single array and de-convert
    # afterwards
    if isinstance(images, list):
        nb_shapes = len(set([image.shape for image in images]))
        if nb_shapes == 1:
            return list(imresize_many_images(np.array(images), sizes=sizes, interpolation=interpolation))
        else:
            return [imresize_many_images(image[np.newaxis, ...], sizes=sizes, interpolation=interpolation)[0, ...]
                    for image in images]

    shape = images.shape
    do_assert(images.ndim in [3, 4], "Expected array of shape (N, H, W, [C]), got shape %s" % (str(shape),))
    nb_images = shape[0]
    im_height, im_width = shape[1], shape[2]
    nb_channels = shape[3] if images.ndim > 3 else None

    height, width = sizes[0], sizes[1]
    height = int(np.round(im_height * height)) if is_single_float(height) else height
    width = int(np.round(im_width * width)) if is_single_float(width) else width

    if height == im_height and width == im_width:
        return np.copy(images)

    ip = interpolation
    do_assert(ip is None or ip in IMRESIZE_VALID_INTERPOLATIONS)
    if ip is None:
        if height > im_height or width > im_width:
            ip = cv2.INTER_AREA
        else:
            ip = cv2.INTER_LINEAR
    elif ip in ["nearest", cv2.INTER_NEAREST]:
        ip = cv2.INTER_NEAREST
    elif ip in ["linear", cv2.INTER_LINEAR]:
        ip = cv2.INTER_LINEAR
    elif ip in ["area", cv2.INTER_AREA]:
        ip = cv2.INTER_AREA
    else:  # if ip in ["cubic", cv2.INTER_CUBIC]:
        ip = cv2.INTER_CUBIC

    # TODO find more beautiful way to avoid circular imports
    from . import dtypes as iadt
    if ip == cv2.INTER_NEAREST:
        iadt.gate_dtypes(images,
                         allowed=["bool", "uint8", "uint16", "int8", "int16", "int32", "float16", "float32", "float64"],
                         disallowed=["uint32", "uint64", "uint128", "uint256", "int64", "int128", "int256",
                                     "float96", "float128", "float256"],
                         augmenter=None)
    else:
        iadt.gate_dtypes(images,
                         allowed=["bool", "uint8", "uint16", "int8", "int16", "float16", "float32", "float64"],
                         disallowed=["uint32", "uint64", "uint128", "uint256", "int32", "int64", "int128", "int256",
                                     "float96", "float128", "float256"],
                         augmenter=None)

    result_shape = (nb_images, height, width)
    if nb_channels is not None:
        result_shape = result_shape + (nb_channels,)
    result = np.zeros(result_shape, dtype=images.dtype)
    for i, image in enumerate(images):
        input_dtype = image.dtype
        if image.dtype.type == np.bool_:
            image = image.astype(np.uint8) * 255
        elif image.dtype.type == np.int8 and ip != cv2.INTER_NEAREST:
            image = image.astype(np.int16)
        elif image.dtype.type == np.float16:
            image = image.astype(np.float32)

        result_img = cv2.resize(image, (width, height), interpolation=ip)
        assert result_img.dtype == image.dtype

        # cv2 removes the channel axis if input was (H, W, 1)
        # we re-add it (but only if input was not (H, W))
        if len(result_img.shape) == 2 and nb_channels is not None and nb_channels == 1:
            result_img = result_img[:, :, np.newaxis]

        if input_dtype.type == np.bool_:
            result_img = result_img > 127
        elif input_dtype.type == np.int8 and ip != cv2.INTER_NEAREST:
            # TODO somehow better avoid circular imports here
            from . import dtypes as iadt
            result_img = iadt.restore_dtypes_(result_img, np.int8)
        elif input_dtype.type == np.float16:
            # TODO see above
            from . import dtypes as iadt
            result_img = iadt.restore_dtypes_(result_img, np.float16)
        result[i] = result_img
    return result