def AdditiveGaussianNoise(loc=0, scale=0, per_channel=False, name=None, deterministic=False, random_state=None):
    """
    Add gaussian noise (aka white noise) to images.

    dtype support::

        See ``imgaug.augmenters.arithmetic.AddElementwise``.

    Parameters
    ----------
    loc : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Mean of the normal distribution that generates the noise.

            * If a number, exactly that value will be used.
            * If a tuple ``(a, b)``, a random value from the range ``a <= x <= b`` will
              be sampled per image.
            * If a list, then a random value will be sampled from that list per
              image.
            * If a StochasticParameter, a value will be sampled from the
              parameter per image.

    scale : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Standard deviation of the normal distribution that generates the noise.
        Must be ``>= 0``. If 0 then only `loc` will be used.

            * If an int or float, exactly that value will be used.
            * If a tuple ``(a, b)``, a random value from the range ``a <= x <= b`` will
              be sampled per image.
            * If a list, then a random value will be sampled from that list per
              image.
            * If a StochasticParameter, a value will be sampled from the
              parameter per image.

    per_channel : bool or float, optional
        Whether to use the same noise value per pixel for all channels (False)
        or to sample a new value for each channel (True).
        If this value is a float ``p``, then for ``p`` percent of all images
        `per_channel` will be treated as True, otherwise as False.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = iaa.AdditiveGaussianNoise(scale=0.1*255)

    adds gaussian noise from the distribution ``N(0, 0.1*255)`` to images.

    >>> aug = iaa.AdditiveGaussianNoise(scale=(0, 0.1*255))

    adds gaussian noise from the distribution ``N(0, s)`` to images,
    where s is sampled per image from the range ``0 <= s <= 0.1*255``.

    >>> aug = iaa.AdditiveGaussianNoise(scale=0.1*255, per_channel=True)

    adds gaussian noise from the distribution ``N(0, 0.1*255)`` to images,
    where the noise value is different per pixel *and* channel (e.g. a
    different one for red, green and blue channels for the same pixel).

    >>> aug = iaa.AdditiveGaussianNoise(scale=0.1*255, per_channel=0.5)

    adds gaussian noise from the distribution ``N(0, 0.1*255)`` to images,
    where the noise value is sometimes (50 percent of all cases) the same
    per pixel for all channels and sometimes different (other 50 percent).

    """
    loc2 = iap.handle_continuous_param(loc, "loc", value_range=None, tuple_to_uniform=True, list_to_choice=True)
    scale2 = iap.handle_continuous_param(scale, "scale", value_range=(0, None), tuple_to_uniform=True,
                                         list_to_choice=True)

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return AddElementwise(iap.Normal(loc=loc2, scale=scale2), per_channel=per_channel, name=name,
                          deterministic=deterministic, random_state=random_state)