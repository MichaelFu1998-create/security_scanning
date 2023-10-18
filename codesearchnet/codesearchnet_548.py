def affine_transform_cv2(x, transform_matrix, flags=None, border_mode='constant'):
    """Return transformed images by given an affine matrix in OpenCV format (x is width). (Powered by OpenCV2, faster than ``tl.prepro.affine_transform``)

    Parameters
    ----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    transform_matrix : numpy.array
        A transform matrix, OpenCV format.
    border_mode : str
        - `constant`, pad the image with a constant value (i.e. black or 0)
        - `replicate`, the row or column at the very edge of the original is replicated to the extra border.

    Examples
    --------
    >>> M_shear = tl.prepro.affine_shear_matrix(intensity=0.2, is_random=False)
    >>> M_zoom = tl.prepro.affine_zoom_matrix(zoom_range=0.8)
    >>> M_combined = M_shear.dot(M_zoom)
    >>> result = tl.prepro.affine_transform_cv2(image, M_combined)
    """
    rows, cols = x.shape[0], x.shape[1]
    if flags is None:
        flags = cv2.INTER_AREA
    if border_mode is 'constant':
        border_mode = cv2.BORDER_CONSTANT
    elif border_mode is 'replicate':
        border_mode = cv2.BORDER_REPLICATE
    else:
        raise Exception("unsupport border_mode, check cv.BORDER_ for more details.")
    return cv2.warpAffine(x, transform_matrix[0:2,:], \
            (cols,rows), flags=flags, borderMode=border_mode)