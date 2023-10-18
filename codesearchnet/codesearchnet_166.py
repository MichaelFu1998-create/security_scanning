def quokka_segmentation_map(size=None, extract=None):
    """
    Returns a segmentation map for the standard example quokka image.

    Parameters
    ----------
    size : None or float or tuple of int, optional
        See :func:`imgaug.quokka`.

    extract : None or 'square' or tuple of number or imgaug.BoundingBox or imgaug.BoundingBoxesOnImage
        See :func:`imgaug.quokka`.

    Returns
    -------
    result : imgaug.SegmentationMapOnImage
        Segmentation map object.

    """
    # TODO get rid of this deferred import
    from imgaug.augmentables.segmaps import SegmentationMapOnImage

    with open(QUOKKA_ANNOTATIONS_FP, "r") as f:
        json_dict = json.load(f)

    xx = []
    yy = []
    for kp_dict in json_dict["polygons"][0]["keypoints"]:
        x = kp_dict["x"]
        y = kp_dict["y"]
        xx.append(x)
        yy.append(y)

    img_seg = np.zeros((643, 960, 1), dtype=np.float32)
    rr, cc = skimage.draw.polygon(np.array(yy), np.array(xx), shape=img_seg.shape)
    img_seg[rr, cc] = 1.0

    if extract is not None:
        bb = _quokka_normalize_extract(extract)
        img_seg = bb.extract_from_image(img_seg)

    segmap = SegmentationMapOnImage(img_seg, shape=img_seg.shape[0:2] + (3,))

    if size is not None:
        shape_resized = _compute_resized_shape(img_seg.shape, size)
        segmap = segmap.resize(shape_resized[0:2])
        segmap.shape = tuple(shape_resized[0:2]) + (3,)

    return segmap