def compute_paddings_for_aspect_ratio(arr, aspect_ratio):
    """
    Compute the amount of pixels by which an array has to be padded to fulfill an aspect ratio.

    The aspect ratio is given as width/height.
    Depending on which dimension is smaller (height or width), only the corresponding
    sides (left/right or top/bottom) will be padded. In each case, both of the sides will
    be padded equally.

    Parameters
    ----------
    arr : (H,W) ndarray or (H,W,C) ndarray
        Image-like array for which to compute pad amounts.

    aspect_ratio : float
        Target aspect ratio, given as width/height. E.g. 2.0 denotes the image having twice
        as much width as height.

    Returns
    -------
    result : tuple of int
        Required paddign amounts to reach the target aspect ratio, given as a tuple
        of the form ``(top, right, bottom, left)``.

    """
    do_assert(arr.ndim in [2, 3])
    do_assert(aspect_ratio > 0)
    height, width = arr.shape[0:2]
    do_assert(height > 0)
    aspect_ratio_current = width / height

    pad_top = 0
    pad_right = 0
    pad_bottom = 0
    pad_left = 0

    if aspect_ratio_current < aspect_ratio:
        # vertical image, height > width
        diff = (aspect_ratio * height) - width
        pad_right = int(np.ceil(diff / 2))
        pad_left = int(np.floor(diff / 2))
    elif aspect_ratio_current > aspect_ratio:
        # horizontal image, width > height
        diff = ((1/aspect_ratio) * width) - height
        pad_top = int(np.floor(diff / 2))
        pad_bottom = int(np.ceil(diff / 2))

    return pad_top, pad_right, pad_bottom, pad_left