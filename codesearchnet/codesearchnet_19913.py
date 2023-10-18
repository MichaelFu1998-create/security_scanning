def fread(f,byteLocation,structFormat=None,nBytes=1):
    """
    Given an already-open (rb mode) file object, return a certain number of bytes at a specific location.
    If a struct format is given, calculate the number of bytes required and return the object it represents.
    """
    f.seek(byteLocation)
    if structFormat:
        val = struct.unpack(structFormat, f.read(struct.calcsize(structFormat)))
        val = val[0] if len(val)==1 else list(val)
        return val
    else:
        return f.read(nBytes)