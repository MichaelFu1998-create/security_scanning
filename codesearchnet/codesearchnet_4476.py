def serialize_object(obj, buffer_threshold=MAX_BYTES, item_threshold=MAX_ITEMS):
    """Serialize an object into a list of sendable buffers.

    Parameters
    ----------

    obj : object
        The object to be serialized
    buffer_threshold : int
        The threshold (in bytes) for pulling out data buffers
        to avoid pickling them.
    item_threshold : int
        The maximum number of items over which canning will iterate.
        Containers (lists, dicts) larger than this will be pickled without
        introspection.

    Returns
    -------
    [bufs] : list of buffers representing the serialized object.
    """
    buffers = []
    if istype(obj, sequence_types) and len(obj) < item_threshold:
        cobj = can_sequence(obj)
        for c in cobj:
            buffers.extend(_extract_buffers(c, buffer_threshold))
    elif istype(obj, dict) and len(obj) < item_threshold:
        cobj = {}
        for k in sorted(obj):
            c = can(obj[k])
            buffers.extend(_extract_buffers(c, buffer_threshold))
            cobj[k] = c
    else:
        cobj = can(obj)
        buffers.extend(_extract_buffers(cobj, buffer_threshold))

    buffers.insert(0, pickle.dumps(cobj, PICKLE_PROTOCOL))
    return buffers