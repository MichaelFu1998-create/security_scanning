def Crop(px=None, percent=None, keep_size=True, sample_independently=True,
         name=None, deterministic=False, random_state=None):
    """
    Augmenter that crops/cuts away pixels at the sides of the image.

    That allows to cut out subimages from given (full) input images.
    The number of pixels to cut off may be defined in absolute values or
    percent of the image sizes.

    dtype support::

        See ``imgaug.augmenters.size.CropAndPad``.

    Parameters
    ----------
    px : None or int or imgaug.parameters.StochasticParameter or tuple, optional
        The number of pixels to crop away (cut off) on each side of the image.
        Either this or the parameter `percent` may be set, not both at the same
        time.

            * If None, then pixel-based cropping will not be used.
            * If int, then that exact number of pixels will always be cropped.
            * If StochasticParameter, then that parameter will be used for each
              image. Four samples will be drawn per image (top, right, bottom,
              left).
            * If a tuple of two ints with values ``a`` and ``b``, then each
              side will be cropped by a random amount in the range
              ``a <= x <= b``. ``x`` is sampled per image side.
            * If a tuple of four entries, then the entries represent top, right,
              bottom, left. Each entry may be a single integer (always crop by
              exactly that value), a tuple of two ints ``a`` and ``b`` (crop by
              an amount ``a <= x <= b``), a list of ints (crop by a random
              value that is contained in the list) or a StochasticParameter
              (sample the amount to crop from that parameter).

    percent : None or int or float or imgaug.parameters.StochasticParameter \
              or tuple, optional
        The number of pixels to crop away (cut off) on each side of the image
        given *in percent* of the image height/width.
        E.g. if this is set to 0.1, the augmenter will always crop away
        10 percent of the image's height at the top, 10 percent of the width
        on the right, 10 percent of the height at the bottom and 10 percent
        of the width on the left.
        Either this or the parameter `px` may be set, not both at the same time.

            * If None, then percent-based cropping will not be used.
            * If int, then expected to be 0 (no cropping).
            * If float, then that percentage will always be cropped away.
            * If StochasticParameter, then that parameter will be used for each
              image. Four samples will be drawn per image (top, right, bottom,
              left).
            * If a tuple of two floats with values ``a`` and ``b``, then each
              side will be cropped by a random percentage in the range
              ``a <= x <= b``. ``x`` is sampled per image side.
            * If a tuple of four entries, then the entries represent top, right,
              bottom, left. Each entry may be a single float (always crop by
              exactly that percent value), a tuple of two floats a and ``b``
              (crop by a percentage ``a <= x <= b``), a list of floats (crop by
              a random value that is contained in the list) or a
              StochasticParameter (sample the percentage to crop from that
              parameter).

    keep_size : bool, optional
        After cropping, the result image has a different height/width than
        the input image. If this parameter is set to True, then the cropped
        image will be resized to the input image's size, i.e. the image size
        is then not changed by the augmenter.

    sample_independently : bool, optional
        If False AND the values for `px`/`percent` result in exactly one
        probability distribution for the amount to crop, only one
        single value will be sampled from that probability distribution
        and used for all sides. I.e. the crop amount then is the same
        for all sides.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = iaa.Crop(px=(0, 10))

    crops each side by a random value from the range 0px to 10px (the value
    is sampled per side).

    >>> aug = iaa.Crop(px=(0, 10), sample_independently=False)

    samples one value ``v`` from the discrete range ``[0..10]`` and crops all
    sides by ``v`` pixels.

    >>> aug = iaa.Crop(px=(0, 10), keep_size=False)

    crops each side by a random value from the range 0px to 10px (the value
    is sampled per side). After cropping, the images are NOT resized to their
    original size (i.e. the images may end up having different heights/widths).

    >>> aug = iaa.Crop(px=((0, 10), (0, 5), (0, 10), (0, 5)))

    crops the top and bottom by a random value from the range 0px to 10px
    and the left and right by a random value in the range 0px to 5px.

    >>> aug = iaa.Crop(percent=(0, 0.1))

    crops each side by a random value from the range 0 percent to
    10 percent. (Percent with respect to the side's size, e.g. for the
    top side it uses the image's height.)

    >>> aug = iaa.Crop(percent=([0.05, 0.1], [0.05, 0.1], [0.05, 0.1], [0.05, 0.1]))

    crops each side by either 5 percent or 10 percent.

    """

    def recursive_negate(v):
        if v is None:
            return v
        elif ia.is_single_number(v):
            ia.do_assert(v >= 0)
            return -v
        elif isinstance(v, iap.StochasticParameter):
            return iap.Multiply(v, -1)
        elif isinstance(v, tuple):
            return tuple([recursive_negate(v_) for v_ in v])
        elif isinstance(v, list):
            return [recursive_negate(v_) for v_ in v]
        else:
            raise Exception("Expected None or int or float or StochasticParameter or list or tuple, got %s." % (
                type(v),))

    px = recursive_negate(px)
    percent = recursive_negate(percent)

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    aug = CropAndPad(
        px=px, percent=percent,
        keep_size=keep_size, sample_independently=sample_independently,
        name=name, deterministic=deterministic, random_state=random_state
    )
    return aug