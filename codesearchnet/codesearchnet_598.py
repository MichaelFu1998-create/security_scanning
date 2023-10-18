def obj_box_zoom(
        im, classes=None, coords=None, zoom_range=(0.9,
                                                   1.1), row_index=0, col_index=1, channel_index=2, fill_mode='nearest',
        cval=0., order=1, is_rescale=False, is_center=False, is_random=False, thresh_wh=0.02, thresh_wh2=12.
):
    """Zoom in and out of a single image, randomly or non-randomly, and compute the new bounding box coordinates.
    Objects outside the cropped image will be removed.

    Parameters
    -----------
    im : numpy.array
        An image with dimension of [row, col, channel] (default).
    classes : list of int or None
        Class IDs.
    coords : list of list of 4 int/float or None
        Coordinates [[x, y, w, h], [x, y, w, h], ...].
    zoom_range row_index col_index channel_index is_random fill_mode cval and order : see ``tl.prepro.zoom``.
    is_rescale : boolean
        Set to True, if the input coordinates are rescaled to [0, 1]. Default is False.
    is_center : boolean
        Set to True, if the x and y of coordinates are the centroid. (i.e. darknet format). Default is False.
    thresh_wh : float
        Threshold, remove the box if its ratio of width(height) to image size less than the threshold.
    thresh_wh2 : float
        Threshold, remove the box if its ratio of width to height or vice verse higher than the threshold.

    Returns
    -------
    numpy.array
        A processed image
    list of int
        A list of classes
    list of list of 4 numbers
        A list of new bounding boxes.

    """
    if classes is None:
        classes = []
    if coords is None:
        coords = []

    if len(zoom_range) != 2:
        raise Exception('zoom_range should be a tuple or list of two floats. ' 'Received arg: ', zoom_range)
    if is_random:
        if zoom_range[0] == 1 and zoom_range[1] == 1:
            zx, zy = 1, 1
            tl.logging.info(" random_zoom : not zoom in/out")
        else:
            zx, zy = np.random.uniform(zoom_range[0], zoom_range[1], 2)
    else:
        zx, zy = zoom_range
    # tl.logging.info(zx, zy)
    zoom_matrix = np.array([[zx, 0, 0], [0, zy, 0], [0, 0, 1]])

    h, w = im.shape[row_index], im.shape[col_index]
    transform_matrix = transform_matrix_offset_center(zoom_matrix, h, w)
    im_new = affine_transform(im, transform_matrix, channel_index, fill_mode, cval, order)

    # modified from obj_box_crop
    def _get_coord(coord):
        """Input pixel-unit [x, y, w, h] format, then make sure [x, y] it is the up-left coordinates,
        before getting the new coordinates.
        Boxes outsides the cropped image will be removed.

        """
        if is_center:
            coord = obj_box_coord_centroid_to_upleft(coord)

        # ======= pixel unit format and upleft, w, h ==========
        x = (coord[0] - im.shape[1] / 2) / zy + im.shape[1] / 2  # only change this
        y = (coord[1] - im.shape[0] / 2) / zx + im.shape[0] / 2  # only change this
        w = coord[2] / zy  # only change this
        h = coord[3] / zx  # only change thisS

        if x < 0:
            if x + w <= 0:
                return None
            w = w + x
            x = 0
        elif x > im_new.shape[1]:  # object outside the cropped image
            return None

        if y < 0:
            if y + h <= 0:
                return None
            h = h + y
            y = 0
        elif y > im_new.shape[0]:  # object outside the cropped image
            return None

        if (x is not None) and (x + w > im_new.shape[1]):  # box outside the cropped image
            w = im_new.shape[1] - x

        if (y is not None) and (y + h > im_new.shape[0]):  # box outside the cropped image
            h = im_new.shape[0] - y

        if (w / (h + 1.) > thresh_wh2) or (h / (w + 1.) > thresh_wh2):  # object shape strange: too narrow
            # tl.logging.info('xx', w, h)
            return None

        if (w / (im_new.shape[1] * 1.) < thresh_wh) or (h / (im_new.shape[0] * 1.) <
                                                        thresh_wh):  # object shape strange: too narrow
            # tl.logging.info('yy', w, im_new.shape[1], h, im_new.shape[0])
            return None

        coord = [x, y, w, h]

        # convert back if input format is center.
        if is_center:
            coord = obj_box_coord_upleft_to_centroid(coord)

        return coord

    coords_new = list()
    classes_new = list()
    for i, _ in enumerate(coords):
        coord = coords[i]

        if len(coord) != 4:
            raise AssertionError("coordinate should be 4 values : [x, y, w, h]")

        if is_rescale:
            # for scaled coord, upscaled before process and scale back in the end.
            coord = obj_box_coord_scale_to_pixelunit(coord, im.shape)
            coord = _get_coord(coord)
            if coord is not None:
                coord = obj_box_coord_rescale(coord, im_new.shape)
                coords_new.append(coord)
                classes_new.append(classes[i])
        else:
            coord = _get_coord(coord)
            if coord is not None:
                coords_new.append(coord)
                classes_new.append(classes[i])
    return im_new, classes_new, coords_new