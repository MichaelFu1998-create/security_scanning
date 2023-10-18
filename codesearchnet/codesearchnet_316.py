def MotionBlur(k=5, angle=(0, 360), direction=(-1.0, 1.0), order=1, name=None, deterministic=False, random_state=None):
    """
    Augmenter that sharpens images and overlays the result with the original image.

    dtype support::

        See ``imgaug.augmenters.convolutional.Convolve``.

    Parameters
    ----------
    k : int or tuple of int or list of int or imgaug.parameters.StochasticParameter, optional
        Kernel size to use.

            * If a single int, then that value will be used for the height
              and width of the kernel.
            * If a tuple of two ints ``(a, b)``, then the kernel size will be
              sampled from the interval ``[a..b]``.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then ``N`` samples will be drawn from
              that parameter per ``N`` input images, each representing the kernel
              size for the nth image.

    angle : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Angle of the motion blur in degrees (clockwise, relative to top center direction).

            * If a number, exactly that value will be used.
            * If a tuple ``(a, b)``, a random value from the range ``a <= x <= b`` will
              be sampled per image.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, a value will be sampled from the
              parameter per image.

    direction : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Forward/backward direction of the motion blur. Lower values towards -1.0 will point the motion blur towards
        the back (with angle provided via `angle`). Higher values towards 1.0 will point the motion blur forward.
        A value of 0.0 leads to a uniformly (but still angled) motion blur.

            * If a number, exactly that value will be used.
            * If a tuple ``(a, b)``, a random value from the range ``a <= x <= b`` will
              be sampled per image.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, a value will be sampled from the
              parameter per image.

    order : int or iterable of int or imgaug.ALL or imgaug.parameters.StochasticParameter, optional
        Interpolation order to use when rotating the kernel according to `angle`.
        See :func:`imgaug.augmenters.geometric.Affine.__init__`.
        Recommended to be ``0`` or ``1``, with ``0`` being faster, but less continuous/smooth as `angle` is changed,
        particularly around multiple of 45 degrees.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = iaa.MotionBlur(k=15)

    Create a motion blur augmenter with kernel size of 15x15.

    >>> aug = iaa.MotionBlur(k=15, angle=[-45, 45])

    Create a motion blur augmenter with kernel size of 15x15 and a blur angle of either -45 or 45 degrees (randomly
    picked per image).

    """
    # TODO allow (1, None) and set to identity matrix if k == 1
    k_param = iap.handle_discrete_param(k, "k", value_range=(3, None), tuple_to_uniform=True, list_to_choice=True,
                                        allow_floats=False)
    angle_param = iap.handle_continuous_param(angle, "angle", value_range=None, tuple_to_uniform=True,
                                              list_to_choice=True)
    direction_param = iap.handle_continuous_param(direction, "direction", value_range=(-1.0-1e-6, 1.0+1e-6),
                                                  tuple_to_uniform=True, list_to_choice=True)

    def create_matrices(image, nb_channels, random_state_func):
        # avoid cyclic import between blur and geometric
        from . import geometric as iaa_geometric

        # force discrete for k_sample via int() in case of stochastic parameter
        k_sample = int(k_param.draw_sample(random_state=random_state_func))
        angle_sample = angle_param.draw_sample(random_state=random_state_func)
        direction_sample = direction_param.draw_sample(random_state=random_state_func)

        k_sample = k_sample if k_sample % 2 != 0 else k_sample + 1
        direction_sample = np.clip(direction_sample, -1.0, 1.0)
        direction_sample = (direction_sample + 1.0) / 2.0

        matrix = np.zeros((k_sample, k_sample), dtype=np.float32)
        matrix[:, k_sample//2] = np.linspace(float(direction_sample), 1.0 - float(direction_sample), num=k_sample)
        rot = iaa_geometric.Affine(rotate=angle_sample, order=order)
        matrix = (rot.augment_image((matrix * 255).astype(np.uint8)) / 255.0).astype(np.float32)

        return [matrix/np.sum(matrix)] * nb_channels

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return iaa_convolutional.Convolve(create_matrices, name=name, deterministic=deterministic,
                                      random_state=random_state)