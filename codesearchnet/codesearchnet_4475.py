def _restore_buffers(obj, buffers):
    """Restore extracted buffers."""
    if isinstance(obj, CannedObject) and obj.buffers:
        for i, buf in enumerate(obj.buffers):
            if buf is None:
                obj.buffers[i] = buffers.pop(0)