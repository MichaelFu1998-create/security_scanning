def Snowflakes(density=(0.005, 0.075), density_uniformity=(0.3, 0.9), flake_size=(0.2, 0.7),
               flake_size_uniformity=(0.4, 0.8), angle=(-30, 30), speed=(0.007, 0.03),
               name=None, deterministic=False, random_state=None):
    """
    Augmenter to add falling snowflakes to images.

    This is a wrapper around ``SnowflakesLayer``. It executes 1 to 3 layers per image.

    dtype support::

        * ``uint8``: yes; tested
        * ``uint16``: no (1)
        * ``uint32``: no (1)
        * ``uint64``: no (1)
        * ``int8``: no (1)
        * ``int16``: no (1)
        * ``int32``: no (1)
        * ``int64``: no (1)
        * ``float16``: no (1)
        * ``float32``: no (1)
        * ``float64``: no (1)
        * ``float128``: no (1)
        * ``bool``: no (1)

        - (1) Parameters of this augmenter are optimized for the value range of uint8.
              While other dtypes may be accepted, they will lead to images augmented in
              ways inappropriate for the respective dtype.

    Parameters
    ----------
    density : number or tuple of number or list of number or imgaug.parameters.StochasticParameter
        Density of the snowflake layer, as a probability of each pixel in low resolution space to be a snowflake.
        Valid value range is ``(0.0, 1.0)``. Recommended to be around ``(0.01, 0.075)``.

            * If a number, then that value will be used for all images.
            * If a tuple ``(a, b)``, then a value from the continuous range ``[a, b]`` will be used.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then a value will be sampled per image from that parameter.

    density_uniformity : number or tuple of number or list of number or imgaug.parameters.StochasticParameter
        Size uniformity of the snowflakes. Higher values denote more similarly sized snowflakes.
        Valid value range is ``(0.0, 1.0)``. Recommended to be around ``0.5``.

            * If a number, then that value will be used for all images.
            * If a tuple ``(a, b)``, then a value from the continuous range ``[a, b]`` will be used.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then a value will be sampled per image from that parameter.

    flake_size : number or tuple of number or list of number or imgaug.parameters.StochasticParameter
        Size of the snowflakes. This parameter controls the resolution at which snowflakes are sampled.
        Higher values mean that the resolution is closer to the input image's resolution and hence each sampled
        snowflake will be smaller (because of the smaller pixel size).

        Valid value range is ``[0.0, 1.0)``. Recommended values:

            * On ``96x128`` a value of ``(0.1, 0.4)`` worked well.
            * On ``192x256`` a value of ``(0.2, 0.7)`` worked well.
            * On ``960x1280`` a value of ``(0.7, 0.95)`` worked well.

        Allowed datatypes:

            * If a number, then that value will be used for all images.
            * If a tuple ``(a, b)``, then a value from the continuous range ``[a, b]`` will be used.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then a value will be sampled per image from that parameter.

    flake_size_uniformity : number or tuple of number or list of number or imgaug.parameters.StochasticParameter
        Controls the size uniformity of the snowflakes. Higher values mean that the snowflakes are more similarly
        sized. Valid value range is ``(0.0, 1.0)``. Recommended to be around ``0.5``.

            * If a number, then that value will be used for all images.
            * If a tuple ``(a, b)``, then a value from the continuous range ``[a, b]`` will be used.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then a value will be sampled per image from that parameter.

    angle : number or tuple of number or list of number or imgaug.parameters.StochasticParameter
        Angle in degrees of motion blur applied to the snowflakes, where ``0.0`` is motion blur that points straight
        upwards. Recommended to be around ``(-30, 30)``.
        See also :func:`imgaug.augmenters.blur.MotionBlur.__init__`.

            * If a number, then that value will be used for all images.
            * If a tuple ``(a, b)``, then a value from the continuous range ``[a, b]`` will be used.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then a value will be sampled per image from that parameter.

    speed : number or tuple of number or list of number or imgaug.parameters.StochasticParameter
        Perceived falling speed of the snowflakes. This parameter controls the motion blur's kernel size.
        It follows roughly the form ``kernel_size = image_size * speed``. Hence,
        Values around ``1.0`` denote that the motion blur should "stretch" each snowflake over the whole image.

        Valid value range is ``(0.0, 1.0)``. Recommended values:

            * On ``96x128`` a value of ``(0.01, 0.05)`` worked well.
            * On ``192x256`` a value of ``(0.007, 0.03)`` worked well.
            * On ``960x1280`` a value of ``(0.001, 0.03)`` worked well.


        Allowed datatypes:

            * If a number, then that value will be used for all images.
            * If a tuple ``(a, b)``, then a value from the continuous range ``[a, b]`` will be used.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then a value will be sampled per image from that parameter.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = iaa.Snowflakes(flake_size=(0.1, 0.4), speed=(0.01, 0.05))

    Adds snowflakes to small images (around ``96x128``).

    >>> aug = iaa.Snowflakes(flake_size=(0.2, 0.7), speed=(0.007, 0.03))

    Adds snowflakes to medium-sized images (around ``192x256``).

    >>> aug = iaa.Snowflakes(flake_size=(0.7, 0.95), speed=(0.001, 0.03))

    Adds snowflakes to large images (around ``960x1280``).

    """
    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    layer = SnowflakesLayer(
        density=density, density_uniformity=density_uniformity,
        flake_size=flake_size, flake_size_uniformity=flake_size_uniformity,
        angle=angle, speed=speed,
        blur_sigma_fraction=(0.0001, 0.001)
    )

    return meta.SomeOf(
        (1, 3), children=[layer.deepcopy() for _ in range(3)],
        random_order=False, name=name, deterministic=deterministic, random_state=random_state
    )