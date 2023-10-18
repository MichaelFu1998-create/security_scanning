def binary_erosion(x, radius=3):
    """Return binary morphological erosion of an image,
    see `skimage.morphology.binary_erosion <http://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.binary_erosion>`__.

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
    x = _binary_erosion(x, selem=mask)
    return x