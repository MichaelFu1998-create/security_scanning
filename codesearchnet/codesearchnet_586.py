def erosion(x, radius=3):
    """Return greyscale morphological erosion of an image,
    see `skimage.morphology.erosion <http://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.erosion>`__.

    Parameters
    -----------
    x : 2D array
        A greyscale image.
    radius : int
        For the radius of mask.

    Returns
    -------
    numpy.array
        A processed greyscale image.

    """
    mask = disk(radius)
    x = _erosion(x, selem=mask)
    return x