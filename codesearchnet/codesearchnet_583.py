def binary_dilation(x, radius=3):
    """Return fast binary morphological dilation of an image.
    see `skimage.morphology.binary_dilation <http://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.binary_dilation>`__.

    Parameters
    -----------
    x : 2D array
        A binary image.
    radius : int
        For the radius of mask.

    Returns
    -------
    numpy.array
        A processed binary image.

    """
    mask = disk(radius)
    x = _binary_dilation(x, selem=mask)

    return x