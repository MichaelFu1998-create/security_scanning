def _extract_buffers(obj, threshold=MAX_BYTES):
    """Extract buffers larger than a certain threshold."""
    buffers = []
    if isinstance(obj, CannedObject) and obj.buffers:
        for i, buf in enumerate(obj.buffers):
            nbytes = _nbytes(buf)
            if nbytes > threshold:
                # buffer larger than threshold, prevent pickling
                obj.buffers[i] = None
                buffers.append(buf)
            # buffer too small for separate send, coerce to bytes
            # because pickling buffer objects just results in broken pointers
            elif isinstance(buf, memoryview):
                obj.buffers[i] = buf.tobytes()
            elif isinstance(buf, buffer):
                obj.buffers[i] = bytes(buf)
    return buffers