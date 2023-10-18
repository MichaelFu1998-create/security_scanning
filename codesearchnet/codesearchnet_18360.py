def sha256file(abspath, nbytes=0, chunk_size=DEFAULT_CHUNK_SIZE):
    """
    Return sha256 hash value of a piece of a file

    Estimate processing time on:

    :param abspath: the absolute path to the file
    :param nbytes: only has first N bytes of the file. if 0 or None,
      hash all file
    """
    return get_file_fingerprint(abspath, hashlib.sha256, nbytes=nbytes, chunk_size=chunk_size)