def checksum(file_path, hash_type='md5', block_size=65536):
    """Returns either the md5 or sha256 hash of a file at `file_path`.
    
    md5 is the default hash_type as it is faster than sha256

    The default block size is 64 kb, which appears to be one of a few command
    choices according to https://stackoverflow.com/a/44873382/2680. The code
    below is an extension of the example presented in that post.
    """
    if hash_type == 'md5':
        hash_ = hashlib.md5()
    elif hash_type == 'sha256':
        hash_ = hashlib.sha256()
    else:
        raise ValueError(
            "{} is an invalid hash_type. Expected 'md5' or 'sha256'."
            .format(hash_type)
        )

    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hash_.update(block)
    return hash_.hexdigest()