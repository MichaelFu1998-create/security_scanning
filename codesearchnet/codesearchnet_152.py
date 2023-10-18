def CoarsePepper(p=0, size_px=None, size_percent=None, per_channel=False, min_size=4, name=None, deterministic=False,
                 random_state=None):
    """
    Adds coarse pepper noise to an image, i.e. rectangles that contain noisy black-ish pixels.

    dtype support::

        See ``imgaug.augmenters.arithmetic.ReplaceElementwise``.

    Parameters
    ----------
    p : float or tuple of float or list of float or imgaug.parameters.StochasticParameter, optional
        Probability of changing a pixel to pepper noise.

            * If a float, then that value will be used for all images as the
              probability.
            * If a tuple ``(a, b)``, then a probability will be sampled per image
              from the range ``a <= x <= b.``
            * If a list, then a random value will be sampled from that list
              per image.
            * If a StochasticParameter, then this parameter will be used as
              the *mask*, i.e. it is expected to contain values between
              0.0 and 1.0, where 1.0 means that pepper is to be added
              at that location.

    size_px : int or tuple of int or imgaug.parameters.StochasticParameter, optional
        The size of the lower resolution image from which to sample the noise
        mask in absolute pixel dimensions.

            * If an integer, then that size will be used for both height and
              width. E.g. a value of 3 would lead to a ``3x3`` mask, which is then
              upsampled to ``HxW``, where ``H`` is the image size and W the image width.
            * If a tuple ``(a, b)``, then two values ``M``, ``N`` will be sampled from the
              range ``[a..b]`` and the mask will be generated at size ``MxN``, then
              upsampled to ``HxW``.
            * If a StochasticParameter, then this parameter will be used to
              determine the sizes. It is expected to be discrete.

    size_percent : float or tuple of float or imgaug.parameters.StochasticParameter, optional
        The size of the lower resolution image from which to sample the noise
        mask *in percent* of the input image.

            * If a float, then that value will be used as the percentage of the
              height and width (relative to the original size). E.g. for value
              p, the mask will be sampled from ``(p*H)x(p*W)`` and later upsampled
              to ``HxW``.
            * If a tuple ``(a, b)``, then two values ``m``, ``n`` will be sampled from the
              interval ``(a, b)`` and used as the percentages, i.e the mask size
              will be ``(m*H)x(n*W)``.
            * If a StochasticParameter, then this parameter will be used to
              sample the percentage values. It is expected to be continuous.

    per_channel : bool or float, optional
        Whether to use the same value (is dropped / is not dropped)
        for all channels of a pixel (False) or to sample a new value for each
        channel (True).
        If this value is a float ``p``, then for ``p`` percent of all images
        `per_channel` will be treated as True, otherwise as False.

    min_size : int, optional
        Minimum size of the low resolution mask, both width and height. If
        `size_percent` or `size_px` leads to a lower value than this, `min_size`
        will be used instead. This should never have a value of less than 2,
        otherwise one may end up with a 1x1 low resolution mask, leading easily
        to the whole image being replaced.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = iaa.CoarsePepper(0.05, size_percent=(0.01, 0.1))

    Replaces 5 percent of all pixels with pepper in an image that has
    1 to 10 percent of the input image size, then upscales the results
    to the input image size, leading to large rectangular areas being replaced.

    """
    mask = iap.handle_probability_param(p, "p", tuple_to_uniform=True, list_to_choice=True)

    if size_px is not None:
        mask_low = iap.FromLowerResolution(other_param=mask, size_px=size_px, min_size=min_size)
    elif size_percent is not None:
        mask_low = iap.FromLowerResolution(other_param=mask, size_percent=size_percent, min_size=min_size)
    else:
        raise Exception("Either size_px or size_percent must be set.")

    replacement01 = iap.ForceSign(
        iap.Beta(0.5, 0.5) - 0.5,
        positive=False,
        mode="invert"
    ) + 0.5
    replacement = replacement01 * 255

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return ReplaceElementwise(
        mask=mask_low,
        replacement=replacement,
        per_channel=per_channel,
        name=name,
        deterministic=deterministic,
        random_state=random_state
    )