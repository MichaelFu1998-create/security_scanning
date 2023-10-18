def md5file(abspath, nbytes=0, chunk_size=DEFAULT_CHUNK_SIZE):
    """
    Return md5 hash value of a piece of a file

    Estimate processing time on:

    :param abspath: the absolute path to the file
    :param nbytes: only has first N bytes of the file. if 0 or None,
      hash all file

    CPU = i7-4600U 2.10GHz - 2.70GHz, RAM = 8.00 GB
    1 second can process 0.25GB data

    - 0.59G - 2.43 sec
    - 1.3G - 5.68 sec
    - 1.9G - 7.72 sec
    - 2.5G - 10.32 sec
    - 3.9G - 16.0 sec
    """
    return get_file_fingerprint(abspath, hashlib.md5, nbytes=nbytes, chunk_size=chunk_size)