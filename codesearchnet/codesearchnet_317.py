def Clouds(name=None, deterministic=False, random_state=None):
    """
    Augmenter to draw clouds in images.

    This is a wrapper around ``CloudLayer``. It executes 1 to 2 layers per image, leading to varying densities
    and frequency patterns of clouds.

    This augmenter seems to be fairly robust w.r.t. the image size. Tested with ``96x128``, ``192x256``
    and ``960x1280``.

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
    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> aug = iaa.Clouds()

    Creates an augmenter that adds clouds to images.

    """
    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return meta.SomeOf((1, 2), children=[
        CloudLayer(
            intensity_mean=(196, 255), intensity_freq_exponent=(-2.5, -2.0), intensity_coarse_scale=10,
            alpha_min=0, alpha_multiplier=(0.25, 0.75), alpha_size_px_max=(2, 8), alpha_freq_exponent=(-2.5, -2.0),
            sparsity=(0.8, 1.0), density_multiplier=(0.5, 1.0)
        ),
        CloudLayer(
            intensity_mean=(196, 255), intensity_freq_exponent=(-2.0, -1.0), intensity_coarse_scale=10,
            alpha_min=0, alpha_multiplier=(0.5, 1.0), alpha_size_px_max=(64, 128), alpha_freq_exponent=(-2.0, -1.0),
            sparsity=(1.0, 1.4), density_multiplier=(0.8, 1.5)
        )
    ], random_order=False, name=name, deterministic=deterministic, random_state=random_state)