def unpickle(filepath):
    """Decompress and unpickle."""
    arr = []
    with open(filepath, 'rb') as f:
        carr = f.read(blosc.MAX_BUFFERSIZE)
        while len(carr) > 0:
            arr.append(blosc.decompress(carr))
            carr = f.read(blosc.MAX_BUFFERSIZE)
    return pkl.loads(b"".join(arr))