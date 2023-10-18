def DirectedEdgeDetect(alpha=0, direction=(0.0, 1.0), name=None, deterministic=False, random_state=None):
    """
    Augmenter that detects edges that have certain directions and marks them
    in a black and white image and then overlays the result with the original
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

    direction : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Angle of edges to pronounce, where 0 represents 0 degrees and 1.0
        represents 360 degrees (both clockwise, starting at the top).
        Default value is ``(0.0, 1.0)``, i.e. pick a random angle per image.

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
    >>> aug = DirectedEdgeDetect(alpha=1.0, direction=0)

    turns input images into edge images in which edges are detected from
    top side of the image (i.e. the top sides of horizontal edges are
    added to the output).

    >>> aug = DirectedEdgeDetect(alpha=1.0, direction=90/360)

    same as before, but detecting edges from the right (right side of each
    vertical edge).

    >>> aug = DirectedEdgeDetect(alpha=1.0, direction=(0.0, 1.0))

    same as before, but detecting edges from a variable direction (anything
    between 0 and 1.0, i.e. 0 degrees and 360 degrees, starting from the
    top and moving clockwise).

    >>> aug = DirectedEdgeDetect(alpha=(0.0, 0.3), direction=0)

    generates edge images (edges detected from the top) and overlays them
    with the input images by a variable amount between 0 and 30 percent
    (e.g. for 0.3 then ``0.7*old_image + 0.3*edge_image``).

    """
    alpha_param = iap.handle_continuous_param(alpha, "alpha", value_range=(0, 1.0), tuple_to_uniform=True,
                                              list_to_choice=True)
    direction_param = iap.handle_continuous_param(direction, "direction", value_range=None, tuple_to_uniform=True,
                                                  list_to_choice=True)

    def create_matrices(_image, nb_channels, random_state_func):
        alpha_sample = alpha_param.draw_sample(random_state=random_state_func)
        ia.do_assert(0 <= alpha_sample <= 1.0)
        direction_sample = direction_param.draw_sample(random_state=random_state_func)

        deg = int(direction_sample * 360) % 360
        rad = np.deg2rad(deg)
        x = np.cos(rad - 0.5*np.pi)
        y = np.sin(rad - 0.5*np.pi)
        direction_vector = np.array([x, y])

        matrix_effect = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ], dtype=np.float32)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if (x, y) != (0, 0):
                    cell_vector = np.array([x, y])
                    distance_deg = np.rad2deg(ia.angle_between_vectors(cell_vector, direction_vector))
                    distance = distance_deg / 180
                    similarity = (1 - distance)**4
                    matrix_effect[y+1, x+1] = similarity
        matrix_effect = matrix_effect / np.sum(matrix_effect)
        matrix_effect = matrix_effect * (-1)
        matrix_effect[1, 1] = 1

        matrix_nochange = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], dtype=np.float32)

        matrix = (1-alpha_sample) * matrix_nochange + alpha_sample * matrix_effect

        return [matrix] * nb_channels

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return Convolve(create_matrices, name=name, deterministic=deterministic, random_state=random_state)