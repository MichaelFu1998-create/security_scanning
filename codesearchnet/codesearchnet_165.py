def quokka_heatmap(size=None, extract=None):
    """
    Returns a heatmap (here: depth map) for the standard example quokka image.

    Parameters
    ----------
    size : None or float or tuple of int, optional
        See :func:`imgaug.quokka`.

    extract : None or 'square' or tuple of number or imgaug.BoundingBox or imgaug.BoundingBoxesOnImage
        See :func:`imgaug.quokka`.

    Returns
    -------
    result : imgaug.HeatmapsOnImage
        Depth map as an heatmap object. Values close to 0.0 denote objects that are close to
        the camera. Values close to 1.0 denote objects that are furthest away (among all shown
        objects).

    """
    # TODO get rid of this deferred import
    from imgaug.augmentables.heatmaps import HeatmapsOnImage

    img = imageio.imread(QUOKKA_DEPTH_MAP_HALFRES_FP, pilmode="RGB")
    img = imresize_single_image(img, (643, 960), interpolation="cubic")

    if extract is not None:
        bb = _quokka_normalize_extract(extract)
        img = bb.extract_from_image(img)
    if size is None:
        size = img.shape[0:2]

    shape_resized = _compute_resized_shape(img.shape, size)
    img = imresize_single_image(img, shape_resized[0:2])
    img_0to1 = img[..., 0]  # depth map was saved as 3-channel RGB
    img_0to1 = img_0to1.astype(np.float32) / 255.0
    img_0to1 = 1 - img_0to1  # depth map was saved as 0 being furthest away

    return HeatmapsOnImage(img_0to1, shape=img_0to1.shape[0:2] + (3,))