def pickle(obj, filepath):
    """Pickle and compress."""
    arr = pkl.dumps(obj, -1)
    with open(filepath, 'wb') as f:
        s = 0
        while s < len(arr):
            e = min(s + blosc.MAX_BUFFERSIZE, len(arr))
            carr = blosc.compress(arr[s:e], typesize=8)
            f.write(carr)
            s = e