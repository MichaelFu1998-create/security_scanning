def quokka(size=None, extract=None):
    """
    Returns an image of a quokka as a numpy array.

    Parameters
    ----------
    size : None or float or tuple of int, optional
        Size of the output image. Input into :func:`imgaug.imgaug.imresize_single_image`.
        Usually expected to be a tuple ``(H, W)``, where ``H`` is the desired height
        and ``W`` is the width. If None, then the image will not be resized.

    extract : None or 'square' or tuple of number or imgaug.BoundingBox or imgaug.BoundingBoxesOnImage
        Subarea of the quokka image to extract:

            * If None, then the whole image will be used.
            * If string ``square``, then a squared area ``(x: 0 to max 643, y: 0 to max 643)`` will
              be extracted from the image.
            * If a tuple, then expected to contain four numbers denoting ``x1``, ``y1``, ``x2``
              and ``y2``.
            * If a BoundingBox, then that bounding box's area will be extracted from the image.
            * If a BoundingBoxesOnImage, then expected to contain exactly one bounding box
              and a shape matching the full image dimensions (i.e. ``(643, 960, *)``). Then the
              one bounding box will be used similar to BoundingBox.

    Returns
    -------
    img : (H,W,3) ndarray
        The image array of dtype uint8.

    """
    img = imageio.imread(QUOKKA_FP, pilmode="RGB")
    if extract is not None:
        bb = _quokka_normalize_extract(extract)
        img = bb.extract_from_image(img)
    if size is not None:
        shape_resized = _compute_resized_shape(img.shape, size)
        img = imresize_single_image(img, shape_resized[0:2])
    return img