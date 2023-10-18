def crop(x, wrg, hrg, is_random=False, row_index=0, col_index=1):
    """Randomly or centrally crop an image.

    Parameters
    ----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    wrg : int
        Size of width.
    hrg : int
        Size of height.
    is_random : boolean,
        If True, randomly crop, else central crop. Default is False.
    row_index: int
        index of row.
    col_index: int
        index of column.

    Returns
    -------
    numpy.array
        A processed image.

    """
    h, w = x.shape[row_index], x.shape[col_index]

    if (h < hrg) or (w < wrg):
        raise AssertionError("The size of cropping should smaller than or equal to the original image")

    if is_random:
        h_offset = int(np.random.uniform(0, h - hrg))
        w_offset = int(np.random.uniform(0, w - wrg))
        # tl.logging.info(h_offset, w_offset, x[h_offset: hrg+h_offset ,w_offset: wrg+w_offset].shape)
        return x[h_offset:hrg + h_offset, w_offset:wrg + w_offset]
    else:  # central crop
        h_offset = int(np.floor((h - hrg) / 2.))
        w_offset = int(np.floor((w - wrg) / 2.))
        h_end = h_offset + hrg
        w_end = w_offset + wrg
        return x[h_offset:h_end, w_offset:w_end]