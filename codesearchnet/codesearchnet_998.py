def _hashCoordinate(coordinate):
    """Hash a coordinate to a 64 bit integer."""
    coordinateStr = ",".join(str(v) for v in coordinate)
    # Compute the hash and convert to 64 bit int.
    hash = int(int(hashlib.md5(coordinateStr).hexdigest(), 16) % (2 ** 64))
    return hash