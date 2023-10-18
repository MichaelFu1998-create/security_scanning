async def get_size(media):
    """
        Get the size of a file

    Parameters
    ----------
    media : file object
        The file object of the media

    Returns
    -------
    int
        The size of the file
    """
    if hasattr(media, 'seek'):
        await execute(media.seek(0, os.SEEK_END))
        size = await execute(media.tell())
        await execute(media.seek(0))
    elif hasattr(media, 'headers'):
        size = int(media.headers['Content-Length'])
    elif isinstance(media, bytes):
        size = len(media)
    else:
        raise TypeError("Can't get size of media of type:",
                        type(media).__name__)

    _logger.info("media size: %dB" % size)
    return size