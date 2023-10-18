def pad_to_aspect_ratio(arr, aspect_ratio, mode="constant", cval=0, return_pad_amounts=False):
    """
    Pad an image-like array on its sides so that it matches a target aspect ratio.

    Depending on which dimension is smaller (height or width), only the corresponding
    sides (left/right or top/bottom) will be padded. In each case, both of the sides will
    be padded equally.

    dtype support::

        See :func:`imgaug.imgaug.pad`.

    Parameters
    ----------
    arr : (H,W) ndarray or (H,W,C) ndarray
        Image-like array to pad.

    aspect_ratio : float
        Target aspect ratio, given as width/height. E.g. 2.0 denotes the image having twice
        as much width as height.

    mode : str, optional
        Padding mode to use. See :func:`numpy.pad` for details.

    cval : number, optional
        Value to use for padding if `mode` is ``constant``. See :func:`numpy.pad` for details.

    return_pad_amounts : bool, optional
        If False, then only the padded image will be returned. If True, a tuple with two
        entries will be returned, where the first entry is the padded image and the second
        entry are the amounts by which each image side was padded. These amounts are again a
        tuple of the form (top, right, bottom, left), with each value being an integer.

    Returns
    -------
    arr_padded : (H',W') ndarray or (H',W',C) ndarray
        Padded image as (H',W') or (H',W',C) ndarray, fulfulling the given aspect_ratio.

    tuple of int
        Amounts by which the image was padded on each side, given as a tuple ``(top, right, bottom, left)``.
        This tuple is only returned if `return_pad_amounts` was set to True.
        Otherwise only ``arr_padded`` is returned.

    """
    pad_top, pad_right, pad_bottom, pad_left = compute_paddings_for_aspect_ratio(arr, aspect_ratio)
    arr_padded = pad(
        arr,
        top=pad_top,
        right=pad_right,
        bottom=pad_bottom,
        left=pad_left,
        mode=mode,
        cval=cval
    )

    if return_pad_amounts:
        return arr_padded, (pad_top, pad_right, pad_bottom, pad_left)
    else:
        return arr_padded