def blend_alpha(image_fg, image_bg, alpha, eps=1e-2):
    """
    Blend two images using an alpha blending.

    In an alpha blending, the two images are naively mixed. Let ``A`` be the foreground image
    and ``B`` the background image and ``a`` is the alpha value. Each pixel intensity is then
    computed as ``a * A_ij + (1-a) * B_ij``.

    dtype support::

        * ``uint8``: yes; fully tested
        * ``uint16``: yes; fully tested
        * ``uint32``: yes; fully tested
        * ``uint64``: yes; fully tested (1)
        * ``int8``: yes; fully tested
        * ``int16``: yes; fully tested
        * ``int32``: yes; fully tested
        * ``int64``: yes; fully tested (1)
        * ``float16``: yes; fully tested
        * ``float32``: yes; fully tested
        * ``float64``: yes; fully tested (1)
        * ``float128``: no (2)
        * ``bool``: yes; fully tested (2)

        - (1) Tests show that these dtypes work, but a conversion to float128 happens, which only
              has 96 bits of size instead of true 128 bits and hence not twice as much resolution.
              It is possible that these dtypes result in inaccuracies, though the tests did not
              indicate that.
        - (2) Not available due to the input dtype having to be increased to an equivalent float
              dtype with two times the input resolution.
        - (3) Mapped internally to ``float16``.

    Parameters
    ----------
    image_fg : (H,W,[C]) ndarray
        Foreground image. Shape and dtype kind must match the one of the
        background image.

    image_bg : (H,W,[C]) ndarray
        Background image. Shape and dtype kind must match the one of the
        foreground image.

    alpha : number or iterable of number or ndarray
        The blending factor, between 0.0 and 1.0. Can be interpreted as the opacity of the
        foreground image. Values around 1.0 result in only the foreground image being visible.
        Values around 0.0 result in only the background image being visible.
        Multiple alphas may be provided. In these cases, there must be exactly one alpha per
        channel in the foreground/background image. Alternatively, for ``(H,W,C)`` images,
        either one ``(H,W)`` array or an ``(H,W,C)`` array of alphas may be provided,
        denoting the elementwise alpha value.

    eps : number, optional
        Controls when an alpha is to be interpreted as exactly 1.0 or exactly 0.0, resulting
        in only the foreground/background being visible and skipping the actual computation.

    Returns
    -------
    image_blend : (H,W,C) ndarray
        Blend of foreground and background image.

    """
    assert image_fg.shape == image_bg.shape
    assert image_fg.dtype.kind == image_bg.dtype.kind
    # TODO switch to gate_dtypes()
    assert image_fg.dtype.name not in ["float128"]
    assert image_bg.dtype.name not in ["float128"]

    # TODO add test for this
    input_was_2d = (len(image_fg.shape) == 2)
    if input_was_2d:
        image_fg = np.atleast_3d(image_fg)
        image_bg = np.atleast_3d(image_bg)

    input_was_bool = False
    if image_fg.dtype.kind == "b":
        input_was_bool = True
        # use float32 instead of float16 here because it seems to be faster
        image_fg = image_fg.astype(np.float32)
        image_bg = image_bg.astype(np.float32)

    alpha = np.array(alpha, dtype=np.float64)
    if alpha.size == 1:
        pass
    else:
        if alpha.ndim == 2:
            assert alpha.shape == image_fg.shape[0:2]
            alpha = alpha.reshape((alpha.shape[0], alpha.shape[1], 1))
        elif alpha.ndim == 3:
            assert alpha.shape == image_fg.shape or alpha.shape == image_fg.shape[0:2] + (1,)
        else:
            alpha = alpha.reshape((1, 1, -1))
        if alpha.shape[2] != image_fg.shape[2]:
            alpha = np.tile(alpha, (1, 1, image_fg.shape[2]))

    if not input_was_bool:
        if np.all(alpha >= 1.0 - eps):
            return np.copy(image_fg)
        elif np.all(alpha <= eps):
            return np.copy(image_bg)

    # for efficiency reaons, only test one value of alpha here, even if alpha is much larger
    assert 0 <= alpha.item(0) <= 1.0

    dt_images = iadt.get_minimal_dtype([image_fg, image_bg])

    # doing this only for non-float images led to inaccuracies for large floats values
    isize = dt_images.itemsize * 2
    isize = max(isize, 4)  # at least 4 bytes (=float32), tends to be faster than float16
    dt_blend = np.dtype("f%d" % (isize,))

    if alpha.dtype != dt_blend:
        alpha = alpha.astype(dt_blend)
    if image_fg.dtype != dt_blend:
        image_fg = image_fg.astype(dt_blend)
    if image_bg.dtype != dt_blend:
        image_bg = image_bg.astype(dt_blend)

    # the following is equivalent to
    #     image_blend = alpha * image_fg + (1 - alpha) * image_bg
    # but supposedly faster
    image_blend = image_bg + alpha * (image_fg - image_bg)

    if input_was_bool:
        image_blend = image_blend > 0.5
    else:
        # skip clip, because alpha is expected to be in range [0.0, 1.0] and both images must have same dtype
        # dont skip round, because otherwise it is very unlikely to hit the image's max possible value
        image_blend = iadt.restore_dtypes_(image_blend, dt_images, clip=False, round=True)

    if input_was_2d:
        return image_blend[:, :, 0]
    return image_blend