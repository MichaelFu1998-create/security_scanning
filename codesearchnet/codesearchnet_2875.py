def generate():
    """Generates a random REQID for request"""
    data_bytes = bytearray(random.getrandbits(8) for i in range(REQID.REQID_SIZE))
    return REQID(data_bytes)