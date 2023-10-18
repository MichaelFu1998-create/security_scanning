async def get_media_metadata(data, path=None):
    """
        Get all the file's metadata and read any kind of file object

    Parameters
    ----------
    data : bytes
        first bytes of the file (the mimetype shoudl be guessed from the
        file headers
    path : str, optional
        path to the file

    Returns
    -------
    str
        The mimetype of the media
    str
        The category of the media on Twitter
    """
    if isinstance(data, bytes):
        media_type = await get_type(data, path)

    else:
        raise TypeError("get_metadata input must be a bytes")

    media_category = get_category(media_type)

    _logger.info("media_type: %s, media_category: %s" % (media_type,
                                                         media_category))

    return media_type, media_category