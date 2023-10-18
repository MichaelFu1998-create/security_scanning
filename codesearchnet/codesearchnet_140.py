def Emboss(alpha=0, strength=1, name=None, deterministic=False, random_state=None):
    """
    Augmenter that embosses images and overlays the result with the original
    image.

    The embossed version pronounces highlights and shadows,
    letting the image look as if it was recreated on a metal plate ("embossed").

    dtype support::

        See ``imgaug.augmenters.convolutional.Convolve``.

    Parameters
    ----------
    alpha : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Visibility of the sharpened image. At 0, only the original image is
        visible, at 1.0 only its sharpened version is visible.

            * If an int or float, exactly that value will be used.
            * If a tuple ``(a, b)``, a random value from the range ``a <= x <= b`` will
              be sampled per image.
            * If a list, then a random value will be sampled from that list
              per image.
            * If a StochasticParameter, a value will be sampled from the
              parameter per image.

    strength : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Parameter that controls the strength of the embossing.
        Sane values are somewhere in the range ``(0, 2)`` with 1 being the standard
        embossing effect. Default value is 1.

            * If an int or float, exactly that value will be used.
            * If a tuple ``(a, b)``, a random value from the range ``a <= x <= b`` will
              be sampled per image.
            * If a list, then a random value will be sampled from that list
              per image.
            * If a StochasticParameter, a value will be sampled from the
              parameter per image.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = Emboss(alpha=(0.0, 1.0), strength=(0.5, 1.5))

    embosses an image with a variable strength in the range ``0.5 <= x <= 1.5``
    and overlays the result with a variable alpha in the range ``0.0 <= a <= 1.0``
    over the old image.

    """
    alpha_param = iap.handle_continuous_param(alpha, "alpha", value_range=(0, 1.0), tuple_to_uniform=True,
                                              list_to_choice=True)
    strength_param = iap.handle_continuous_param(strength, "strength", value_range=(0, None), tuple_to_uniform=True,
                                                 list_to_choice=True)

    def create_matrices(image, nb_channels, random_state_func):
        alpha_sample = alpha_param.draw_sample(random_state=random_state_func)
        ia.do_assert(0 <= alpha_sample <= 1.0)
        strength_sample = strength_param.draw_sample(random_state=random_state_func)
        matrix_nochange = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], dtype=np.float32)
        matrix_effect = np.array([
            [-1-strength_sample, 0-strength_sample, 0],
            [0-strength_sample, 1, 0+strength_sample],
            [0, 0+strength_sample, 1+strength_sample]
        ], dtype=np.float32)
        matrix = (1-alpha_sample) * matrix_nochange + alpha_sample * matrix_effect
        return [matrix] * nb_channels

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return Convolve(create_matrices, name=name, deterministic=deterministic, random_state=random_state)