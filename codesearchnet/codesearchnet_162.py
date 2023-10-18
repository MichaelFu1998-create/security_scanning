def _quokka_normalize_extract(extract):
    """
    Generate a normalized rectangle to be extract from the standard quokka image.

    Parameters
    ----------
    extract : 'square' or tuple of number or imgaug.BoundingBox or imgaug.BoundingBoxesOnImage
        Unnormalized representation of the image subarea to be extracted.

            * If string ``square``, then a squared area ``(x: 0 to max 643, y: 0 to max 643)``
              will be extracted from the image.
            * If a tuple, then expected to contain four numbers denoting ``x1``, ``y1``, ``x2``
              and ``y2``.
            * If a BoundingBox, then that bounding box's area will be extracted from the image.
            * If a BoundingBoxesOnImage, then expected to contain exactly one bounding box
              and a shape matching the full image dimensions (i.e. (643, 960, *)). Then the
              one bounding box will be used similar to BoundingBox.

    Returns
    -------
    bb : imgaug.BoundingBox
        Normalized representation of the area to extract from the standard quokka image.

    """
    # TODO get rid of this deferred import
    from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

    if extract == "square":
        bb = BoundingBox(x1=0, y1=0, x2=643, y2=643)
    elif isinstance(extract, tuple) and len(extract) == 4:
        bb = BoundingBox(x1=extract[0], y1=extract[1], x2=extract[2], y2=extract[3])
    elif isinstance(extract, BoundingBox):
        bb = extract
    elif isinstance(extract, BoundingBoxesOnImage):
        do_assert(len(extract.bounding_boxes) == 1)
        do_assert(extract.shape[0:2] == (643, 960))
        bb = extract.bounding_boxes[0]
    else:
        raise Exception(
            "Expected 'square' or tuple of four entries or BoundingBox or BoundingBoxesOnImage "
            + "for parameter 'extract', got %s." % (type(extract),)
        )
    return bb