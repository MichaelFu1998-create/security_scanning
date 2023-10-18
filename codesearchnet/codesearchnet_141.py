def EdgeDetect(alpha=0, name=None, deterministic=False, random_state=None):
    """
    Augmenter that detects all edges in images, marks them in
    a black and white image and then overlays the result with the original
    image.

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

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = EdgeDetect(alpha=(0.0, 1.0))

    detects edges in an image  and overlays the result with a variable alpha
    in the range ``0.0 <= a <= 1.0`` over the old image.

    """
    alpha_param = iap.handle_continuous_param(alpha, "alpha", value_range=(0, 1.0), tuple_to_uniform=True,
                                              list_to_choice=True)

    def create_matrices(_image, nb_channels, random_state_func):
        alpha_sample = alpha_param.draw_sample(random_state=random_state_func)
        ia.do_assert(0 <= alpha_sample <= 1.0)
        matrix_nochange = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], dtype=np.float32)
        matrix_effect = np.array([
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ], dtype=np.float32)
        matrix = (1-alpha_sample) * matrix_nochange + alpha_sample * matrix_effect
        return [matrix] * nb_channels

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return Convolve(create_matrices, name=name, deterministic=deterministic, random_state=random_state)