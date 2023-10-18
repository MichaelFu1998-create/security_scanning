def OneOf(children, name=None, deterministic=False, random_state=None):
    """
    Augmenter that always executes exactly one of its children.

    dtype support::

        See ``imgaug.augmenters.meta.SomeOf``.

    Parameters
    ----------
    children : list of imgaug.augmenters.meta.Augmenter
        The choices of augmenters to apply.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> imgs = [np.ones((10, 10))]
    >>> seq = iaa.OneOf([
    >>>     iaa.Fliplr(1.0),
    >>>     iaa.Flipud(1.0)
    >>> ])
    >>> imgs_aug = seq.augment_images(imgs)

    flips each image either horizontally or vertically.


    >>> seq = iaa.OneOf([
    >>>     iaa.Fliplr(1.0),
    >>>     iaa.Sequential([
    >>>         iaa.GaussianBlur(1.0),
    >>>         iaa.Dropout(0.05),
    >>>         iaa.AdditiveGaussianNoise(0.1*255)
    >>>     ]),
    >>>     iaa.Noop()
    >>> ])
    >>> imgs_aug = seq.augment_images(imgs)

    either flips each image horizontally, or adds blur+dropout+noise or does
    nothing.

    """
    return SomeOf(n=1, children=children, random_order=False, name=name, deterministic=deterministic,
                  random_state=random_state)