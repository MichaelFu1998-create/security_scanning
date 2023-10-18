def draw_boxes_and_labels_to_image(
        image, classes, coords, scores, classes_list, is_center=True, is_rescale=True, save_name=None
):
    """Draw bboxes and class labels on image. Return or save the image with bboxes, example in the docs of ``tl.prepro``.

    Parameters
    -----------
    image : numpy.array
        The RGB image [height, width, channel].
    classes : list of int
        A list of class ID (int).
    coords : list of int
        A list of list for coordinates.
            - Should be [x, y, x2, y2] (up-left and botton-right format)
            - If [x_center, y_center, w, h] (set is_center to True).
    scores : list of float
        A list of score (float). (Optional)
    classes_list : list of str
        for converting ID to string on image.
    is_center : boolean
        Whether the coordinates is [x_center, y_center, w, h]
            - If coordinates are [x_center, y_center, w, h], set it to True for converting it to [x, y, x2, y2] (up-left and botton-right) internally.
            - If coordinates are [x1, x2, y1, y2], set it to False.
    is_rescale : boolean
        Whether to rescale the coordinates from pixel-unit format to ratio format.
            - If True, the input coordinates are the portion of width and high, this API will scale the coordinates to pixel unit internally.
            - If False, feed the coordinates with pixel unit format.
    save_name : None or str
        The name of image file (i.e. image.png), if None, not to save image.

    Returns
    -------
    numpy.array
        The saved image.

    References
    -----------
    - OpenCV rectangle and putText.
    - `scikit-image <http://scikit-image.org/docs/dev/api/skimage.draw.html#skimage.draw.rectangle>`__.

    """
    if len(coords) != len(classes):
        raise AssertionError("number of coordinates and classes are equal")

    if len(scores) > 0 and len(scores) != len(classes):
        raise AssertionError("number of scores and classes are equal")

    # don't change the original image, and avoid error https://stackoverflow.com/questions/30249053/python-opencv-drawing-errors-after-manipulating-array-with-numpy
    image = image.copy()

    imh, imw = image.shape[0:2]
    thick = int((imh + imw) // 430)

    for i, _v in enumerate(coords):
        if is_center:
            x, y, x2, y2 = tl.prepro.obj_box_coord_centroid_to_upleft_butright(coords[i])
        else:
            x, y, x2, y2 = coords[i]

        if is_rescale:  # scale back to pixel unit if the coords are the portion of width and high
            x, y, x2, y2 = tl.prepro.obj_box_coord_scale_to_pixelunit([x, y, x2, y2], (imh, imw))

        cv2.rectangle(
            image,
            (int(x), int(y)),
            (int(x2), int(y2)),  # up-left and botton-right
            [0, 255, 0],
            thick
        )

        cv2.putText(
            image,
            classes_list[classes[i]] + ((" %.2f" % (scores[i])) if (len(scores) != 0) else " "),
            (int(x), int(y)),  # button left
            0,
            1.5e-3 * imh,  # bigger = larger font
            [0, 0, 256],  # self.meta['colors'][max_indx],
            int(thick / 2) + 1
        )  # bold

    if save_name is not None:
        # cv2.imwrite('_my.png', image)
        save_image(image, save_name)
    # if len(coords) == 0:
    #     tl.logging.info("draw_boxes_and_labels_to_image: no bboxes exist, cannot draw !")
    return image