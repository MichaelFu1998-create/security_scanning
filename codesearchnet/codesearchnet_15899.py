def _create_struct(data, session):
    """Create a struct from session data.
    """
    out = Struct()
    for name in data.dtype.names:
        item = data[name]
        # Extract values that are cells (they are doubly wrapped).
        if isinstance(item, np.ndarray) and item.dtype.kind == 'O':
            item = item.squeeze().tolist()
        out[name] = _extract(item, session)
    return out