def zoom_multi(x, zoom_range=(0.9, 1.1), flags=None, border_mode='constant'):
    """Zoom in and out of images with the same arguments, randomly or non-randomly.
    Usually be used for image segmentation which x=[X, Y], X and Y should be matched.

    Parameters
    -----------
    x : list of numpy.array
        List of images with dimension of [n_images, row, col, channel] (default).
    others : args
        See ``tl.prepro.zoom``.

    Returns
    -------
    numpy.array
        A list of processed images.

    """

    zoom_matrix = affine_zoom_matrix(zoom_range=zoom_range)
    results = []
    for img in x:
        h, w = x.shape[0], x.shape[1]
        transform_matrix = transform_matrix_offset_center(zoom_matrix, h, w)
        results.append(affine_transform_cv2(x, transform_matrix, flags=flags, border_mode=border_mode))
    return result