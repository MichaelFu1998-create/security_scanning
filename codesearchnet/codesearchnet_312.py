def AssertLambda(func_images=None, func_heatmaps=None, func_keypoints=None,
                 func_polygons=None, name=None, deterministic=False,
                 random_state=None):
    """
    Augmenter that runs an assert on each batch of input images
    using a lambda function as condition.

    This is useful to make generic assumption about the input images and error
    out early if they aren't met.

    dtype support::

        * ``uint8``: yes; fully tested
        * ``uint16``: yes; tested
        * ``uint32``: yes; tested
        * ``uint64``: yes; tested
        * ``int8``: yes; tested
        * ``int16``: yes; tested
        * ``int32``: yes; tested
        * ``int64``: yes; tested
        * ``float16``: yes; tested
        * ``float32``: yes; tested
        * ``float64``: yes; tested
        * ``float128``: yes; tested
        * ``bool``: yes; tested

    Parameters
    ----------
    func_images : None or callable, optional
        The function to call for each batch of images.
        It must follow the form ``function(images, random_state, parents, hooks)``
        and return either True (valid input) or False (invalid input).
        It essentially reuses the interface of
        :func:`imgaug.augmenters.meta.Augmenter._augment_images`.

    func_heatmaps : None or callable, optional
        The function to call for each batch of heatmaps.
        It must follow the form ``function(heatmaps, random_state, parents, hooks)``
        and return either True (valid input) or False (invalid input).
        It essentially reuses the interface of
        :func:`imgaug.augmenters.meta.Augmenter._augment_heatmaps`.

    func_keypoints : None or callable, optional
        The function to call for each batch of keypoints.
        It must follow the form ``function(keypoints_on_images, random_state, parents, hooks)``
        and return either True (valid input) or False (invalid input).
        It essentially reuses the interface of
        :func:`imgaug.augmenters.meta.Augmenter._augment_keypoints`.

    func_polygons : None or callable, optional
        The function to call for each batch of polygons.
        It must follow the form ``function(polygons_on_images, random_state, parents, hooks)``
        and return either True (valid input) or False (invalid input).
        It essentially reuses the interface of
        :func:`imgaug.augmenters.meta.Augmenter._augment_polygons`.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    """
    def func_images_assert(images, random_state, parents, hooks):
        ia.do_assert(func_images(images, random_state, parents, hooks),
                     "Input images did not fulfill user-defined assertion in AssertLambda.")
        return images

    def func_heatmaps_assert(heatmaps, random_state, parents, hooks):
        ia.do_assert(func_heatmaps(heatmaps, random_state, parents, hooks),
                     "Input heatmaps did not fulfill user-defined assertion in AssertLambda.")
        return heatmaps

    def func_keypoints_assert(keypoints_on_images, random_state, parents, hooks):
        ia.do_assert(func_keypoints(keypoints_on_images, random_state, parents, hooks),
                     "Input keypoints did not fulfill user-defined assertion in AssertLambda.")
        return keypoints_on_images

    def func_polygons_assert(polygons_on_images, random_state, parents, hooks):
        ia.do_assert(func_polygons(polygons_on_images, random_state, parents, hooks),
                     "Input polygons did not fulfill user-defined assertion in AssertLambda.")
        return polygons_on_images

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)
    return Lambda(func_images_assert if func_images is not None else None,
                  func_heatmaps_assert if func_heatmaps is not None else None,
                  func_keypoints_assert if func_keypoints is not None else None,
                  func_polygons_assert if func_polygons is not None else None,
                  name=name, deterministic=deterministic, random_state=random_state)