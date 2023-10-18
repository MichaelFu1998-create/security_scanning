def AdditivePoissonNoise(lam=0, per_channel=False, name=None, deterministic=False, random_state=None):
    """
    Create an augmenter to add poisson noise to images.

    Poisson noise is comparable to gaussian noise as in ``AdditiveGaussianNoise``, but the values are sampled from
    a poisson distribution instead of a gaussian distribution. As poisson distributions produce only positive numbers,
    the sign of the sampled values are here randomly flipped.

    Values of around ``10.0`` for `lam` lead to visible noise (for uint8).
    Values of around ``20.0`` for `lam` lead to very visible noise (for uint8).
    It is recommended to usually set `per_channel` to True.

    dtype support::

        See ``imgaug.augmenters.arithmetic.AddElementwise``.

    Parameters
    ----------
    lam : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Lambda parameter of the poisson distribution. Recommended values are around ``0.0`` to ``10.0``.

            * If a number, exactly that value will be used.
            * If a tuple ``(a, b)``, a random value from the range ``a <= x <= b`` will
              be sampled per image.
            * If a list, then a random value will be sampled from that list per image.
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
    >>> aug = iaa.AdditivePoissonNoise(lam=5.0)

    Adds poisson noise sampled from ``Poisson(5.0)`` to images.

    >>> aug = iaa.AdditivePoissonNoise(lam=(0.0, 10.0))

    Adds poisson noise sampled from ``Poisson(x)`` to images, where ``x`` is randomly sampled per image from the
    interval ``[0.0, 10.0]``.

    >>> aug = iaa.AdditivePoissonNoise(lam=5.0, per_channel=True)

    Adds poisson noise sampled from ``Poisson(5.0)`` to images,
    where the values are different per pixel *and* channel (e.g. a
    different one for red, green and blue channels for the same pixel).

    >>> aug = iaa.AdditivePoissonNoise(lam=(0.0, 10.0), per_channel=True)

    Adds poisson noise sampled from ``Poisson(x)`` to images,
    with ``x`` being sampled from ``uniform(0.0, 10.0)`` per image, pixel and channel.
    This is the *recommended* configuration.

    >>> aug = iaa.AdditivePoissonNoise(lam=2, per_channel=0.5)

    Adds poisson noise sampled from the distribution ``Poisson(2)`` to images,
    where the values are sometimes (50 percent of all cases) the same
    per pixel for all channels and sometimes different (other 50 percent).

    """
    lam2 = iap.handle_continuous_param(lam, "lam", value_range=(0, None), tuple_to_uniform=True,
                                       list_to_choice=True)

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return AddElementwise(iap.RandomSign(iap.Poisson(lam=lam2)), per_channel=per_channel, name=name,
                          deterministic=deterministic, random_state=random_state)