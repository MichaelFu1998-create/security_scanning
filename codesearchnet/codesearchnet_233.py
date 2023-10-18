def Pad(px=None, percent=None, pad_mode="constant", pad_cval=0, keep_size=True, sample_independently=True,
        name=None, deterministic=False, random_state=None):
    """
    Augmenter that pads images, i.e. adds columns/rows to them.

    dtype support::

        See ``imgaug.augmenters.size.CropAndPad``.

    Parameters
    ----------
    px : None or int or imgaug.parameters.StochasticParameter or tuple, optional
        The number of pixels to pad on each side of the image.
        Either this or the parameter `percent` may be set, not both at the same
        time.

            * If None, then pixel-based padding will not be used.
            * If int, then that exact number of pixels will always be padded.
            * If StochasticParameter, then that parameter will be used for each
              image. Four samples will be drawn per image (top, right, bottom,
              left).
            * If a tuple of two ints with values a and b, then each side will
              be padded by a random amount in the range ``a <= x <= b``.
              ``x`` is sampled per image side.
            * If a tuple of four entries, then the entries represent top, right,
              bottom, left. Each entry may be a single integer (always pad by
              exactly that value), a tuple of two ints ``a`` and ``b`` (pad by
              an amount ``a <= x <= b``), a list of ints (pad by a random value
              that is contained in the list) or a StochasticParameter (sample
              the amount to pad from that parameter).

    percent : None or int or float or imgaug.parameters.StochasticParameter \
              or tuple, optional
        The number of pixels to pad on each side of the image given
        *in percent* of the image height/width.
        E.g. if this is set to 0.1, the augmenter will always add 10 percent
        of the image's height to the top, 10 percent of the width to the right,
        10 percent of the height at the bottom and 10 percent of the width to
        the left. Either this or the parameter `px` may be set, not both at the
        same time.

            * If None, then percent-based padding will not be used.
            * If int, then expected to be 0 (no padding).
            * If float, then that percentage will always be padded.
            * If StochasticParameter, then that parameter will be used for each
              image. Four samples will be drawn per image (top, right, bottom,
              left).
            * If a tuple of two floats with values a and b, then each side will
              be padded by a random percentage in the range ``a <= x <= b``.
              ``x`` is sampled per image side.
            * If a tuple of four entries, then the entries represent top, right,
              bottom, left. Each entry may be a single float (always pad by
              exactly that percent value), a tuple of two floats ``a`` and ``b``
              (pad by a percentage ``a <= x <= b``), a list of floats (pad by a
              random value that is contained in the list) or a
              StochasticParameter (sample the percentage to pad from that
              parameter).

    pad_mode : imgaug.ALL or str or list of str or \
               imgaug.parameters.StochasticParameter, optional
        Padding mode to use. The available modes match the numpy padding modes,
        i.e. ``constant``, ``edge``, ``linear_ramp``, ``maximum``, ``median``,
        ``minimum``, ``reflect``, ``symmetric``, ``wrap``. The modes
        ``constant`` and ``linear_ramp`` use extra values, which are provided
        by ``pad_cval`` when necessary. See :func:`imgaug.imgaug.pad` for
        more details.

            * If ``imgaug.ALL``, then a random mode from all available modes
              will be sampled per image.
            * If a string, it will be used as the pad mode for all images.
            * If a list of strings, a random one of these will be sampled per
              image and used as the mode.
            * If StochasticParameter, a random mode will be sampled from this
              parameter per image.

    pad_cval : number or tuple of number list of number or \
               imgaug.parameters.StochasticParameter, optional
        The constant value to use if the pad mode is ``constant`` or the end
        value to use if the mode is ``linear_ramp``.
        See :func:`imgaug.imgaug.pad` for more details.

            * If number, then that value will be used.
            * If a tuple of two numbers and at least one of them is a float,
              then a random number will be sampled from the continuous range
              ``a <= x <= b`` and used as the value. If both numbers are
              integers, the range is discrete.
            * If a list of number, then a random value will be chosen from the
              elements of the list and used as the value.
            * If StochasticParameter, a random value will be sampled from that
              parameter per image.

    keep_size : bool, optional
        After padding, the result image will usually have a different
        height/width compared to the original input image. If this parameter is
        set to True, then the padded image will be resized to the input image's
        size, i.e. the augmenter's output shape is always identical to the
        input shape.

    sample_independently : bool, optional
        If False AND the values for `px`/`percent` result in exactly one
        probability distribution for the amount to pad, only one single value
        will be sampled from that probability distribution and used for all
        sides. I.e. the pad amount then is the same for all sides.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = iaa.Pad(px=(0, 10))

    pads each side by a random value from the range 0px to 10px (the value
    is sampled per side). The added rows/columns are filled with black pixels.

    >>> aug = iaa.Pad(px=(0, 10), sample_independently=False)

    samples one value v from the discrete range ``[0..10]`` and pads all sides
    by ``v`` pixels.

    >>> aug = iaa.Pad(px=(0, 10), keep_size=False)

    pads each side by a random value from the range 0px to 10px (the value
    is sampled per side). After padding, the images are NOT resized to their
    original size (i.e. the images may end up having different heights/widths).

    >>> aug = iaa.Pad(px=((0, 10), (0, 5), (0, 10), (0, 5)))

    pads the top and bottom by a random value from the range 0px to 10px
    and the left and right by a random value in the range 0px to 5px.

    >>> aug = iaa.Pad(percent=(0, 0.1))

    pads each side by a random value from the range 0 percent to
    10 percent. (Percent with respect to the side's size, e.g. for the
    top side it uses the image's height.)

    >>> aug = iaa.Pad(percent=([0.05, 0.1], [0.05, 0.1], [0.05, 0.1], [0.05, 0.1]))

    pads each side by either 5 percent or 10 percent.

    >>> aug = iaa.Pad(px=(0, 10), pad_mode="edge")

    pads each side by a random value from the range 0px to 10px (the values
    are sampled per side). The padding uses the ``edge`` mode from numpy's
    pad function.

    >>> aug = iaa.Pad(px=(0, 10), pad_mode=["constant", "edge"])

    pads each side by a random value from the range 0px to 10px (the values
    are sampled per side). The padding uses randomly either the ``constant``
    or ``edge`` mode from numpy's pad function.

    >>> aug = iaa.Pad(px=(0, 10), pad_mode=ia.ALL, pad_cval=(0, 255))

    pads each side by a random value from the range 0px to 10px (the values
    are sampled per side). It uses a random mode for numpy's pad function.
    If the mode is ``constant`` or ``linear_ramp``, it samples a random value
    ``v`` from the range ``[0, 255]`` and uses that as the constant
    value (``mode=constant``) or end value (``mode=linear_ramp``).

    """

    def recursive_validate(v):
        if v is None:
            return v
        elif ia.is_single_number(v):
            ia.do_assert(v >= 0)
            return v
        elif isinstance(v, iap.StochasticParameter):
            return v
        elif isinstance(v, tuple):
            return tuple([recursive_validate(v_) for v_ in v])
        elif isinstance(v, list):
            return [recursive_validate(v_) for v_ in v]
        else:
            raise Exception("Expected None or int or float or StochasticParameter or list or tuple, got %s." % (
                type(v),))

    px = recursive_validate(px)
    percent = recursive_validate(percent)

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    aug = CropAndPad(
        px=px, percent=percent,
        pad_mode=pad_mode, pad_cval=pad_cval,
        keep_size=keep_size, sample_independently=sample_independently,
        name=name, deterministic=deterministic, random_state=random_state
    )
    return aug