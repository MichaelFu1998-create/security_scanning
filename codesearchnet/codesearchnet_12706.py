async def get_type(media, path=None):
    """
    Parameters
    ----------
    media : file object
        A file object of the image
    path : str, optional
        The path to the file

    Returns
    -------
    str
        The mimetype of the media
    str
        The category of the media on Twitter
    """
    if magic:
        if not media:
            raise TypeError("Media data is empty")

        _logger.debug("guessing mimetype using magic")
        media_type = mime.from_buffer(media[:1024])
    else:
        media_type = None
        if path:
            _logger.debug("guessing mimetype using built-in module")
            media_type = mime.guess_type(path)[0]

        if media_type is None:
            msg = ("Could not guess the mimetype of the media.\n"
                   "Please consider installing python-magic\n"
                   "(pip3 install peony-twitter[magic])")
            raise RuntimeError(msg)

    return media_type