def dilation(x, radius=3):
    """Return greyscale morphological dilation of an image,
    see `skimage.morphology.dilation <http://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.dilation>`__.

    Parameters
    -----------
    x : 2D array
        An greyscale image.
    radius : int
        For the radius of mask.

    Returns
    -------
    numpy.array
        A processed greyscale image.

    """
    mask = disk(radius)
    x = dilation(x, selem=mask)

    return x