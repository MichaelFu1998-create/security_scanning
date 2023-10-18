def AssertShape(shape, check_images=True, check_heatmaps=True,
                check_keypoints=True, check_polygons=True,
                name=None, deterministic=False, random_state=None):
    """
    Augmenter to make assumptions about the shape of input image(s), heatmaps and keypoints.

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
    shape : tuple
        The expected shape, given as a tuple. The number of entries in the tuple must match the
        number of dimensions, i.e. it must contain four entries for ``(N, H, W, C)``. If only a
        single image is augmented via ``augment_image()``, then ``N`` is viewed as 1 by this
        augmenter. If the input image(s) don't have a channel axis, then ``C`` is viewed as 1
        by this augmenter.
        Each of the four entries may be None or a tuple of two ints or a list of ints.

            * If an entry is None, any value for that dimensions is accepted.
            * If an entry is int, exactly that integer value will be accepted
              or no other value.
            * If an entry is a tuple of two ints with values ``a`` and ``b``, only a
              value ``x`` with ``a <= x < b`` will be accepted for the dimension.
            * If an entry is a list of ints, only a value for the dimension
              will be accepted which is contained in the list.

    check_images : bool, optional
        Whether to validate input images via the given shape.

    check_heatmaps : bool, optional
        Whether to validate input heatmaps via the given shape.
        The number of heatmaps will be checked and for each Heatmaps
        instance its array's height and width, but not the channel
        count as the channel number denotes the expected number of channels
        in images.

    check_keypoints : bool, optional
        Whether to validate input keypoints via the given shape.
        This will check (a) the number of keypoints and (b) for each
        KeypointsOnImage instance the ``.shape``, i.e. the shape of the
        corresponding image.

    check_polygons : bool, optional
        Whether to validate input keypoints via the given shape.
        This will check (a) the number of polygons and (b) for each
        PolygonsOnImage instance the ``.shape``, i.e. the shape of the
        corresponding image.

    name : None or str, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    deterministic : bool, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    random_state : None or int or numpy.random.RandomState, optional
        See :func:`imgaug.augmenters.meta.Augmenter.__init__`.

    Examples
    --------
    >>> seq = iaa.Sequential([
    >>>     iaa.AssertShape((None, 32, 32, 3)),
    >>>     iaa.Fliplr(0.5)
    >>> ])

    will first check for each image batch, if it contains a variable number of
    ``32x32`` images with 3 channels each. Only if that check succeeds, the
    horizontal flip will be executed (otherwise an assertion error will be
    thrown).

    >>> seq = iaa.Sequential([
    >>>     iaa.AssertShape((None, (32, 64), 32, [1, 3])),
    >>>     iaa.Fliplr(0.5)
    >>> ])

    like above, but now the height may be in the range ``32 <= H < 64`` and
    the number of channels may be either 1 or 3.

    """
    ia.do_assert(len(shape) == 4, "Expected shape to have length 4, got %d with shape: %s." % (len(shape), str(shape)))

    def compare(observed, expected, dimension, image_index):
        if expected is not None:
            if ia.is_single_integer(expected):
                ia.do_assert(observed == expected,
                             "Expected dim %d (entry index: %s) to have value %d, got %d." % (
                                 dimension, image_index, expected, observed))
            elif isinstance(expected, tuple):
                ia.do_assert(len(expected) == 2)
                ia.do_assert(expected[0] <= observed < expected[1],
                             "Expected dim %d (entry index: %s) to have value in range [%d, %d), got %d." % (
                                 dimension, image_index, expected[0], expected[1], observed))
            elif isinstance(expected, list):
                ia.do_assert(any([observed == val for val in expected]),
                             "Expected dim %d (entry index: %s) to have any value of %s, got %d." % (
                                 dimension, image_index, str(expected), observed))
            else:
                raise Exception(("Invalid datatype for shape entry %d, expected each entry to be an integer, "
                                + "a tuple (with two entries) or a list, got %s.") % (dimension, type(expected),))

    def func_images(images, _random_state, _parents, _hooks):
        if check_images:
            if isinstance(images, list):
                if shape[0] is not None:
                    compare(len(images), shape[0], 0, "ALL")

                for i in sm.xrange(len(images)):
                    image = images[i]
                    ia.do_assert(len(image.shape) == 3,
                                 "Expected image number %d to have a shape of length 3, got %d (shape: %s)." % (
                                     i, len(image.shape), str(image.shape)))
                    for j in sm.xrange(len(shape)-1):
                        expected = shape[j+1]
                        observed = image.shape[j]
                        compare(observed, expected, j, i)
            else:
                ia.do_assert(len(images.shape) == 4,
                             "Expected image's shape to have length 4, got %d (shape: %s)." % (
                                 len(images.shape), str(images.shape)))
                for i in range(4):
                    expected = shape[i]
                    observed = images.shape[i]
                    compare(observed, expected, i, "ALL")
        return images

    def func_heatmaps(heatmaps, _random_state, _parents, _hooks):
        if check_heatmaps:
            if shape[0] is not None:
                compare(len(heatmaps), shape[0], 0, "ALL")

            for i in sm.xrange(len(heatmaps)):
                heatmaps_i = heatmaps[i]
                for j in sm.xrange(len(shape[0:2])):
                    expected = shape[j+1]
                    observed = heatmaps_i.arr_0to1.shape[j]
                    compare(observed, expected, j, i)
        return heatmaps

    def func_keypoints(keypoints_on_images, _random_state, _parents, _hooks):
        if check_keypoints:
            if shape[0] is not None:
                compare(len(keypoints_on_images), shape[0], 0, "ALL")

            for i in sm.xrange(len(keypoints_on_images)):
                keypoints_on_image = keypoints_on_images[i]
                for j in sm.xrange(len(shape[0:2])):
                    expected = shape[j+1]
                    observed = keypoints_on_image.shape[j]
                    compare(observed, expected, j, i)
        return keypoints_on_images

    def func_polygons(polygons_on_images, _random_state, _parents, _hooks):
        if check_polygons:
            if shape[0] is not None:
                compare(len(polygons_on_images), shape[0], 0, "ALL")

            for i in sm.xrange(len(polygons_on_images)):
                polygons_on_image = polygons_on_images[i]
                for j in sm.xrange(len(shape[0:2])):
                    expected = shape[j+1]
                    observed = polygons_on_image.shape[j]
                    compare(observed, expected, j, i)
        return polygons_on_images

    if name is None:
        name = "Unnamed%s" % (ia.caller_name(),)

    return Lambda(func_images, func_heatmaps, func_keypoints, func_polygons,
                  name=name, deterministic=deterministic,
                  random_state=random_state)