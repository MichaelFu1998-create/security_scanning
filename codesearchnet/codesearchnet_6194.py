def get_etag(file_path):
    """Return a strong Entity Tag for a (file)path.

    http://www.webdav.org/specs/rfc4918.html#etag

    Returns the following as entity tags::

        Non-file - md5(pathname)
        Win32 - md5(pathname)-lastmodifiedtime-filesize
        Others - inode-lastmodifiedtime-filesize
    """
    # (At least on Vista) os.path.exists returns False, if a file name contains
    # special characters, even if it is correctly UTF-8 encoded.
    # So we convert to unicode. On the other hand, md5() needs a byte string.
    if compat.is_bytes(file_path):
        unicodeFilePath = to_unicode_safe(file_path)
    else:
        unicodeFilePath = file_path
        file_path = file_path.encode("utf8")

    if not os.path.isfile(unicodeFilePath):
        return md5(file_path).hexdigest()

    if sys.platform == "win32":
        statresults = os.stat(unicodeFilePath)
        return (
            md5(file_path).hexdigest()
            + "-"
            + str(statresults[stat.ST_MTIME])
            + "-"
            + str(statresults[stat.ST_SIZE])
        )
    else:
        statresults = os.stat(unicodeFilePath)
        return (
            str(statresults[stat.ST_INO])
            + "-"
            + str(statresults[stat.ST_MTIME])
            + "-"
            + str(statresults[stat.ST_SIZE])
        )