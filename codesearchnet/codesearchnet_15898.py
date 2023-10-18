def _extract(data, session=None):
    """Convert the Octave values to values suitable for Python.
    """
    # Extract each item of a list.
    if isinstance(data, list):
        return [_extract(d, session) for d in data]

    # Ignore leaf objects.
    if not isinstance(data, np.ndarray):
        return data

    # Extract user defined classes.
    if isinstance(data, MatlabObject):
        cls = session._get_user_class(data.classname)
        return cls.from_value(data)

    # Extract struct data.
    if data.dtype.names:
        # Singular struct
        if data.size == 1:
            return _create_struct(data, session)
        # Struct array
        return StructArray(data, session)

    # Extract cells.
    if data.dtype.kind == 'O':
        return Cell(data, session)

    # Compress singleton values.
    if data.size == 1:
        return data.item()

    # Compress empty values.
    if data.size == 0:
        if data.dtype.kind in 'US':
            return ''
        return []

    # Return standard array.
    return data