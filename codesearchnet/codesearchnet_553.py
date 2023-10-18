def crop_multi(x, wrg, hrg, is_random=False, row_index=0, col_index=1):
    """Randomly or centrally crop multiple images.

    Parameters
    ----------
    x : list of numpy.array
        List of images with dimension of [n_images, row, col, channel] (default).
    others : args
        See ``tl.prepro.crop``.

    Returns
    -------
    numpy.array
        A list of processed images.

    """
    h, w = x[0].shape[row_index], x[0].shape[col_index]

    if (h < hrg) or (w < wrg):
        raise AssertionError("The size of cropping should smaller than or equal to the original image")

    if is_random:
        h_offset = int(np.random.uniform(0, h - hrg))
        w_offset = int(np.random.uniform(0, w - wrg))
        results = []
        for data in x:
            results.append(data[h_offset:hrg + h_offset, w_offset:wrg + w_offset])
        return np.asarray(results)
    else:
        # central crop
        h_offset = (h - hrg) / 2
        w_offset = (w - wrg) / 2
        results = []
        for data in x:
            results.append(data[h_offset:h - h_offset, w_offset:w - w_offset])
        return np.asarray(results)