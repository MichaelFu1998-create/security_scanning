def SimplexNoiseAlpha(first=None, second=None, per_channel=False, size_px_max=(2, 16), upscale_method=None,
                      iterations=(1, 3), aggregation_method="max", sigmoid=True, sigmoid_thresh=None,
                      name=None, deterministic=False, random_state=None):
    """
    Augmenter to alpha-blend two image sources using simplex noise alpha masks.

    The alpha masks are sampled using a simplex noise method, roughly creating
    connected blobs of 1s surrounded by 0s. If nearest neighbour upsampling
    is used, these blobs can be rectangular with sharp edges.

    dtype support::

        See ``imgaug.augmenters.blend.AlphaElementwise``.

    Parameters
    ----------
    first : None or imgaug.augmenters.meta.Augmenter or iterable of imgaug.augmenters.meta.Augmenter, optional
        Augmenter(s) that make up the first of the two branches.

            * If None, then the input images will be reused as the output
              of the first branch.
            * If Augmenter, then that augmenter will be used as the branch.
            * If iterable of Augmenter, then that iterable will be converted
              into a Sequential and used as the augmenter.

    second : None or imgaug.augmenters.meta.Augmenter or iterable of imgaug.augmenters.meta.Augmenter, optional
        Augmenter(s) that make up the second of the two branches.

            * If None, then the input images will be reused as the output
              of the second branch.
            * If Augmenter, then that augmenter will be used as the branch.
            * If iterable of Augmenter, then that iterable will be converted
              into a Sequential and used as the augmenter.

    per_channel : bool or float, optional
        Whether to use the same factor for all channels (False)
        or to sample a new value for each channel (True).
        If this value is a float ``p``, then for ``p`` percent of all images
        `per_channel` will be treated as True, otherwise as False.

    size_px_max : int or tuple of int or list of int or imgaug.parameters.StochasticParameter, optional
        The simplex noise is always generated in a low resolution environment.
        This parameter defines the maximum size of that environment (in
        pixels). The environment is initialized at the same size as the input
        image and then downscaled, so that no side exceeds `size_px_max`
        (aspect ratio is kept).

            * If int, then that number will be used as the size for all
              iterations.
            * If tuple of two ints ``(a, b)``, then a value will be sampled
              per iteration from the discrete range ``[a..b]``.
            * If a list of ints, then a value will be picked per iteration at
              random from that list.
            * If a StochasticParameter, then a value will be sampled from
              that parameter per iteration.

    upscale_method : None or imgaug.ALL or str or list of str or imgaug.parameters.StochasticParameter, optional
        After generating the noise maps in low resolution environments, they
        have to be upscaled to the input image size. This parameter controls
        the upscaling method.

            * If None, then either ``nearest`` or ``linear`` or ``cubic`` is picked.
              Most weight is put on linear, followed by cubic.
            * If ia.ALL, then either ``nearest`` or ``linear`` or ``area`` or ``cubic``
              is picked per iteration (all same probability).
            * If string, then that value will be used as the method (must be
              'nearest' or ``linear`` or ``area`` or ``cubic``).
            * If list of string, then a random value will be picked from that
              list per iteration.
            * If StochasticParameter, then a random value will be sampled
              from that parameter per iteration.

    iterations : int or tuple of int or list of int or imgaug.parameters.StochasticParameter, optional
        How often to repeat the simplex noise generation process per image.

            * If int, then that number will be used as the iterations for all
              images.
            * If tuple of two ints ``(a, b)``, then a value will be sampled
              per image from the discrete range ``[a..b]``.
            * If a list of ints, then a value will be picked per image at
              random from that list.
            * If a StochasticParameter, then a value will be sampled from
              that parameter per image.

    aggregation_method : imgaug.ALL or str or list of str or imgaug.parameters.StochasticParameter, optional
        The noise maps (from each iteration) are combined to one noise map
        using an aggregation process. This parameter defines the method used
        for that process. Valid methods are ``min``, ``max`` or ``avg``,
        where ``min`` combines the noise maps by taking the (elementwise) minimum
        over all iteration's results, ``max`` the (elementwise) maximum and
        ``avg`` the (elementwise) average.

            * If imgaug.ALL, then a random value will be picked per image from the
              valid ones.
            * If a string, then that value will always be used as the method.
            * If a list of string, then a random value will be picked from
              that list per image.
            * If a StochasticParameter, then a random value will be sampled
              from that paramter per image.

    sigmoid : bool or number, optional
        Whether to apply a sigmoid function to the final noise maps, resulting
        in maps that have more extreme values (close to 0.0 or 1.0).

            * If bool, then a sigmoid will always (True) or never (False) be
              applied.
            * If a number ``p`` with ``0<=p<=1``, then a sigmoid will be applied to
              ``p`` percent of all final noise maps.

    sigmoid_thresh : None or number or tuple of number or imgaug.parameters.StochasticParameter, optional
        Threshold of the sigmoid, when applied. Thresholds above zero
        (e.g. 5.0) will move the saddle point towards the right, leading to
        more values close to 0.0.

            * If None, then ``Normal(0, 5.0)`` will be used.
            * If number, then that threshold will be used for all images.
            * If tuple of two numbers ``(a, b)``, then a random value will
              be sampled per image from the range ``[a, b]``.
            * If StochasticParameter, then a random value will be sampled from
              that parameter per image.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = iaa.SimplexNoiseAlpha(iaa.EdgeDetect(1.0))

    Detects per image all edges, marks them in a black and white image and
    then alpha-blends the result with the original image using simplex noise
    masks.

    >>> aug = iaa.SimplexNoiseAlpha(iaa.EdgeDetect(1.0), upscale_method="linear")

    Same as the first example, but uses only (smooth) linear upscaling to
    scale the simplex noise masks to the final image sizes, i.e. no nearest
    neighbour upsampling is used, which would result in rectangles with hard
    edges.

    >>> aug = iaa.SimplexNoiseAlpha(iaa.EdgeDetect(1.0), sigmoid_thresh=iap.Normal(10.0, 5.0))

    Same as the first example, but uses a threshold for the sigmoid function
    that is further to the right. This is more conservative, i.e. the generated
    noise masks will be mostly black (values around 0.0), which means that
    most of the original images (parameter/branch `second`) will be kept,
    rather than using the results of the augmentation (parameter/branch
    `first`).

    """
    upscale_method_default = iap.Choice(["nearest", "linear", "cubic"], p=[0.05, 0.6, 0.35])
    sigmoid_thresh_default = iap.Normal(0.0, 5.0)

    noise = iap.SimplexNoise(
        size_px_max=size_px_max,
        upscale_method=upscale_method if upscale_method is not None else upscale_method_default
    )

    if iterations != 1:
        noise = iap.IterativeNoiseAggregator(
            noise,
            iterations=iterations,
            aggregation_method=aggregation_method
        )

    if sigmoid is False or (ia.is_single_number(sigmoid) and sigmoid <= 0.01):
        noise = iap.Sigmoid.create_for_noise(
            noise,
            threshold=sigmoid_thresh if sigmoid_thresh is not None else sigmoid_thresh_default,
            activated=sigmoid
        )

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return AlphaElementwise(
        factor=noise, first=first, second=second, per_channel=per_channel,
        name=name, deterministic=deterministic, random_state=random_state
    )