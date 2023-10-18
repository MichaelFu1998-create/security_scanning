def get_file_hash(fin, block_size=2**20):
    """
    Iteratively builds a file hash without loading the entire file into memory.
    Designed to process an arbitrary binary file.
    """
    if isinstance(fin, six.string_types):
        fin = open(fin)
    h = hashlib.sha512()
    while True:
        data = fin.read(block_size)
        if not data:
            break
        try:
            h.update(data)
        except TypeError:
            # Fixes Python3 error "TypeError: Unicode-objects must be encoded before hashing".
            h.update(data.encode('utf-8'))
    return h.hexdigest()