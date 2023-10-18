def LinearContrast(alpha=1, per_channel=False, name=None, deterministic=False, random_state=None):
    """Adjust contrast by scaling each pixel value to ``127 + alpha*(I_ij-127)``.

    dtype support::

        See :func:`imgaug.augmenters.contrast.adjust_contrast_linear`.

    Parameters
    ----------
    alpha : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Multiplier to linearly pronounce (>1.0), dampen (0.0 to 1.0) or invert (<0.0) the
        difference between each pixel value and the center value, e.g. ``127`` for ``uint8``.

            * If a number, then that value will be used for all images.
            * If a tuple ``(a, b)``, then a value from the range ``[a, b]`` will be used per image.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then a value will be sampled per image from that parameter.

    per_channel :  bool or float, optional
        Whether to use the same value for all channels (False) or to sample a new value for each
        channel (True). If this value is a float ``p``, then for ``p`` percent of all images `per_channel`
        will be treated as True, otherwise as False.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Returns
    -------
    _ContrastFuncWrapper
        Augmenter to perform contrast adjustment by linearly scaling the distance to 128.

    """
    params1d = [
        iap.handle_continuous_param(alpha, "alpha", value_range=None, tuple_to_uniform=True, list_to_choice=True)
    ]
    func = adjust_contrast_linear
    return _ContrastFuncWrapper(
        func, params1d, per_channel,
        dtypes_allowed=["uint8", "uint16", "uint32",
                        "int8", "int16", "int32",
                        "float16", "float32", "float64"],
        dtypes_disallowed=["uint64", "int64", "float96", "float128", "float256", "bool"],
        name=name if name is not None else ia.caller_name(),
        deterministic=deterministic,
        random_state=random_state
    )