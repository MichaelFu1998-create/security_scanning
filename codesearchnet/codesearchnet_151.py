def Pepper(p=0, per_channel=False, name=None, deterministic=False, random_state=None):
    """
    Adds pepper noise to an image, i.e. black-ish pixels.

    This is similar to dropout, but slower and the black pixels are not uniformly black.

    dtype support::

        See ``imgaug.augmenters.arithmetic.ReplaceElementwise``.

    Parameters
    ----------
    p : float or tuple of float or list of float or imgaug.parameters.StochasticParameter, optional
        Probability of changing a pixel to pepper noise.

            * If a float, then that value will be used for all images as the
              probability.
            * If a tuple ``(a, b)``, then a probability will be sampled per image
              from the range ``a <= x <= b``.
            * If a list, then a random value will be sampled from that list
              per image.
            * If a StochasticParameter, then this parameter will be used as
              the *mask*, i.e. it is expected to contain values between
              0.0 and 1.0, where 1.0 means that pepper is to be added
              at that location.

    per_channel : bool or float, optional
        Whether to use the same value for all channels (False)
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
    >>> aug = iaa.Pepper(0.05)

    Replaces 5 percent of all pixels with pepper.

    """

    replacement01 = iap.ForceSign(
        iap.Beta(0.5, 0.5) - 0.5,
        positive=False,
        mode="invert"
    ) + 0.5
    replacement = replacement01 * 255

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return ReplaceElementwise(
        mask=p,
        replacement=replacement,
        per_channel=per_channel,
        name=name,
        deterministic=deterministic,
        random_state=random_state
    )