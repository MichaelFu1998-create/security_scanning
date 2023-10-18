def SigmoidContrast(gain=10, cutoff=0.5, per_channel=False, name=None, deterministic=False, random_state=None):
    """
    Adjust contrast by scaling each pixel value to ``255 * 1/(1 + exp(gain*(cutoff - I_ij/255)))``.

    Values in the range ``gain=(5, 20)`` and ``cutoff=(0.25, 0.75)`` seem to be sensible.

    dtype support::

        See :func:`imgaug.augmenters.contrast.adjust_contrast_sigmoid`.

    Parameters
    ----------
    gain : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Multiplier for the sigmoid function's output.
        Higher values lead to quicker changes from dark to light pixels.

            * If a number, then that value will be used for all images.
            * If a tuple ``(a, b)``, then a value from the range ``[a, b]`` will be used per image.
            * If a list, then a random value will be sampled from that list per image.
            * If a StochasticParameter, then a value will be sampled per image from that parameter.

    cutoff : number or tuple of number or list of number or imgaug.parameters.StochasticParameter, optional
        Cutoff that shifts the sigmoid function in horizontal direction.
        Higher values mean that the switch from dark to light pixels happens later, i.e.
        the pixels will remain darker.

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
        Augmenter to perform sigmoid contrast adjustment.

    """
    # TODO add inv parameter?
    params1d = [
        iap.handle_continuous_param(gain, "gain", value_range=(0, None), tuple_to_uniform=True, list_to_choice=True),
        iap.handle_continuous_param(cutoff, "cutoff", value_range=(0, 1.0), tuple_to_uniform=True, list_to_choice=True)
    ]
    func = adjust_contrast_sigmoid
    return _ContrastFuncWrapper(
        func, params1d, per_channel,
        dtypes_allowed=["uint8", "uint16", "uint32", "uint64",
                        "int8", "int16", "int32", "int64",
                        "float16", "float32", "float64"],
        dtypes_disallowed=["float96", "float128", "float256", "bool"],
        name=name if name is not None else ia.caller_name(),
        deterministic=deterministic,
        random_state=random_state
    )