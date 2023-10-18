def _streaming_file_md5(file_path):
    """
    Create and return a hex checksum using the MD5 sum of the passed in file.
    This will stream the file, rather than load it all into memory.

    :param file_path: full path to the file
    :type file_path: string
    :returns: a hex checksum
    :rtype: string
    """
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        # iter needs an empty byte string for the returned iterator to halt at
        # EOF
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()