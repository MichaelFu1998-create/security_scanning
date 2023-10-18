def _nbytes(buf):
    """Return byte-size of a memoryview or buffer."""
    if isinstance(buf, memoryview):
        if PY3:
            # py3 introduces nbytes attribute
            return buf.nbytes
        else:
            # compute nbytes on py2
            size = buf.itemsize
            for dim in buf.shape:
                size *= dim
            return size
    else:
        # not a memoryview, raw bytes/ py2 buffer
        return len(buf)