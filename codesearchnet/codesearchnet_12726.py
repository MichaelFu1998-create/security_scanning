def optimize_media(file_, max_size, formats):
    """
        Optimize an image
    Resize the picture to the ``max_size``, defaulting to the large
    photo size of Twitter in :meth:`PeonyClient.upload_media` when
    used with the ``optimize_media`` argument.
    Parameters
    ----------
    file_ : file object
        the file object of an image
    max_size : :obj:`tuple` or :obj:`list` of :obj:`int`
        a tuple in the format (width, height) which is maximum size of
        the picture returned by this function
    formats : :obj`list` or :obj:`tuple` of :obj:`dict`
        a list of all the formats to convert the picture to
    Returns
    -------
    file
        The smallest file created in this function
    """
    if not PIL:
        msg = ("Pillow must be installed to optimize a media\n"
               "$ pip3 install Pillow")
        raise RuntimeError(msg)

    img = PIL.Image.open(file_)

    # resize the picture (defaults to the 'large' photo size of Twitter
    # in peony.PeonyClient.upload_media)
    ratio = max(hw / max_hw for hw, max_hw in zip(img.size, max_size))

    if ratio > 1:
        size = tuple(int(hw // ratio) for hw in img.size)
        img = img.resize(size, PIL.Image.ANTIALIAS)

    media = convert(img, formats)

    # do not close a file opened by the user
    # only close if a filename was given
    if not hasattr(file_, 'read'):
        img.close()

    return media