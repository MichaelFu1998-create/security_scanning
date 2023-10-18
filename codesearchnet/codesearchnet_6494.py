def cbuuid_to_uuid(cbuuid):
    """Convert Objective-C CBUUID type to native Python UUID type."""
    data = cbuuid.data().bytes()

    template = '{:0>8}-0000-1000-8000-00805f9b34fb' if len(data) <= 4 else '{:0>32}'
    value = template.format(hexlify(data.tobytes()[:16]).decode('ascii'))
    return uuid.UUID(hex=value)