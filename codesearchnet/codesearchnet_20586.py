def _make_it_3d(img):
    """Enforce that img is a 3D img-like object, if it is not, raise a TypeError.
    i.e., remove dimensions of size 1.

    Parameters
    ----------
    img: numpy.ndarray
        Image data array

    Returns
    -------
    3D numpy ndarray object
    """
    shape = img.shape

    if len(shape) == 3:
        return img

    elif len(shape) == 4 and shape[3] == 1:
        # "squeeze" the image.
        return img[:, :, :, 0]

    else:
        raise TypeError('A 3D image is expected, but an image with a shape of {} was given.'.format(shape))