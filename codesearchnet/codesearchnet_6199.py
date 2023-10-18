def guess_mime_type(url):
    """Use the mimetypes module to lookup the type for an extension.

    This function also adds some extensions required for HTML5
    """
    (mimetype, _mimeencoding) = mimetypes.guess_type(url)
    if not mimetype:
        ext = os.path.splitext(url)[1]
        mimetype = _MIME_TYPES.get(ext)
        _logger.debug("mimetype({}): {}".format(url, mimetype))
    if not mimetype:
        mimetype = "application/octet-stream"
    return mimetype