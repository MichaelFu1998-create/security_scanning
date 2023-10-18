def deserialize_object(buffers, g=None):
    """Reconstruct an object serialized by serialize_object from data buffers.

    Parameters
    ----------

    bufs : list of buffers/bytes

    g : globals to be used when uncanning

    Returns
    -------

    (newobj, bufs) : unpacked object, and the list of remaining unused buffers.
    """
    bufs = list(buffers)
    pobj = buffer_to_bytes_py2(bufs.pop(0))
    canned = pickle.loads(pobj)
    if istype(canned, sequence_types) and len(canned) < MAX_ITEMS:
        for c in canned:
            _restore_buffers(c, bufs)
        newobj = uncan_sequence(canned, g)
    elif istype(canned, dict) and len(canned) < MAX_ITEMS:
        newobj = {}
        for k in sorted(canned):
            c = canned[k]
            _restore_buffers(c, bufs)
            newobj[k] = uncan(c, g)
    else:
        _restore_buffers(canned, bufs)
        newobj = uncan(canned, g)

    return newobj, bufs