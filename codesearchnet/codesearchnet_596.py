def obj_box_crop(
        im, classes=None, coords=None, wrg=100, hrg=100, is_rescale=False, is_center=False, is_random=False,
        thresh_wh=0.02, thresh_wh2=12.
):
    """Randomly or centrally crop an image, and compute the new bounding box coordinates.
    Objects outside the cropped image will be removed.

    Parameters
    -----------
    im : numpy.array
        An image with dimension of [row, col, channel] (default).
    classes : list of int or None
        Class IDs.
    coords : list of list of 4 int/float or None
        Coordinates [[x, y, w, h], [x, y, w, h], ...]
    wrg hrg and is_random : args
        See ``tl.prepro.crop``.
    is_rescale : boolean
        Set to True, if the input coordinates are rescaled to [0, 1]. Default is False.
    is_center : boolean, default False
        Set to True, if the x and y of coordinates are the centroid (i.e. darknet format). Default is False.
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

    h, w = im.shape[0], im.shape[1]

    if (h <= hrg) or (w <= wrg):
        raise AssertionError("The size of cropping should smaller than the original image")

    if is_random:
        h_offset = int(np.random.uniform(0, h - hrg) - 1)
        w_offset = int(np.random.uniform(0, w - wrg) - 1)
        h_end = hrg + h_offset
        w_end = wrg + w_offset
        im_new = im[h_offset:h_end, w_offset:w_end]
    else:  # central crop
        h_offset = int(np.floor((h - hrg) / 2.))
        w_offset = int(np.floor((w - wrg) / 2.))
        h_end = h_offset + hrg
        w_end = w_offset + wrg
        im_new = im[h_offset:h_end, w_offset:w_end]

    #              w
    #   _____________________________
    #   |  h/w offset               |
    #   |       -------             |
    # h |       |     |             |
    #   |       |     |             |
    #   |       -------             |
    #   |            h/w end        |
    #   |___________________________|

    def _get_coord(coord):
        """Input pixel-unit [x, y, w, h] format, then make sure [x, y] it is the up-left coordinates,
        before getting the new coordinates.
        Boxes outsides the cropped image will be removed.

        """
        if is_center:
            coord = obj_box_coord_centroid_to_upleft(coord)

        ##======= pixel unit format and upleft, w, h ==========##

        # x = np.clip( coord[0] - w_offset, 0, w_end - w_offset)
        # y = np.clip( coord[1] - h_offset, 0, h_end - h_offset)
        # w = np.clip( coord[2]           , 0, w_end - w_offset)
        # h = np.clip( coord[3]           , 0, h_end - h_offset)

        x = coord[0] - w_offset
        y = coord[1] - h_offset
        w = coord[2]
        h = coord[3]

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

        ## convert back if input format is center.
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