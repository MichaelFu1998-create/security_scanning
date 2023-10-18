def _get_file_sha1(file):
    """Return the SHA1 hash of the given a file-like object as ``file``.
    This will seek the file back to 0 when it's finished.

    """
    bits = file.read()
    file.seek(0)
    h = hashlib.new('sha1', bits).hexdigest()
    return h