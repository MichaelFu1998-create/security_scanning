def read_image(image, path=''):
    """Read one image.

    Parameters
    -----------
    image : str
        The image file name.
    path : str
        The image folder path.

    Returns
    -------
    numpy.array
        The image.

    """
    return imageio.imread(os.path.join(path, image))