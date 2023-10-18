def obj_box_horizontal_flip(im, coords=None, is_rescale=False, is_center=False, is_random=False):
    """Left-right flip the image and coordinates for object detection.

    Parameters
    ----------
    im : numpy.array
        An image with dimension of [row, col, channel] (default).
    coords : list of list of 4 int/float or None
        Coordinates [[x, y, w, h], [x, y, w, h], ...].
    is_rescale : boolean
        Set to True, if the input coordinates are rescaled to [0, 1]. Default is False.
    is_center : boolean
        Set to True, if the x and y of coordinates are the centroid (i.e. darknet format). Default is False.
    is_random : boolean
        If True, randomly flip. Default is False.

    Returns
    -------
    numpy.array
        A processed image
    list of list of 4 numbers
        A list of new bounding boxes.

    Examples
    --------
    >>> im = np.zeros([80, 100])    # as an image with shape width=100, height=80
    >>> im, coords = obj_box_left_right_flip(im, coords=[[0.2, 0.4, 0.3, 0.3], [0.1, 0.5, 0.2, 0.3]], is_rescale=True, is_center=True, is_random=False)
    >>> print(coords)
      [[0.8, 0.4, 0.3, 0.3], [0.9, 0.5, 0.2, 0.3]]
    >>> im, coords = obj_box_left_right_flip(im, coords=[[0.2, 0.4, 0.3, 0.3]], is_rescale=True, is_center=False, is_random=False)
    >>> print(coords)
      [[0.5, 0.4, 0.3, 0.3]]
    >>> im, coords = obj_box_left_right_flip(im, coords=[[20, 40, 30, 30]], is_rescale=False, is_center=True, is_random=False)
    >>> print(coords)
      [[80, 40, 30, 30]]
    >>> im, coords = obj_box_left_right_flip(im, coords=[[20, 40, 30, 30]], is_rescale=False, is_center=False, is_random=False)
    >>> print(coords)
      [[50, 40, 30, 30]]

    """
    if coords is None:
        coords = []

    def _flip(im, coords):
        im = flip_axis(im, axis=1, is_random=False)
        coords_new = list()

        for coord in coords:

            if len(coord) != 4:
                raise AssertionError("coordinate should be 4 values : [x, y, w, h]")

            if is_rescale:
                if is_center:
                    # x_center' = 1 - x
                    x = 1. - coord[0]
                else:
                    # x_center' = 1 - x - w
                    x = 1. - coord[0] - coord[2]
            else:
                if is_center:
                    # x' = im.width - x
                    x = im.shape[1] - coord[0]
                else:
                    # x' = im.width - x - w
                    x = im.shape[1] - coord[0] - coord[2]
            coords_new.append([x, coord[1], coord[2], coord[3]])
        return im, coords_new

    if is_random:
        factor = np.random.uniform(-1, 1)
        if factor > 0:
            return _flip(im, coords)
        else:
            return im, coords
    else:
        return _flip(im, coords)