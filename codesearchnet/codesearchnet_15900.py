def _encode(data, convert_to_float):
    """Convert the Python values to values suitable to send to Octave.
    """
    ctf = convert_to_float

    # Handle variable pointer.
    if isinstance(data, (OctaveVariablePtr)):
        return _encode(data.value, ctf)

    # Handle a user defined object.
    if isinstance(data, OctaveUserClass):
        return _encode(OctaveUserClass.to_value(data), ctf)

    # Handle a function pointer.
    if isinstance(data, (OctaveFunctionPtr, MatlabFunction)):
        raise Oct2PyError('Cannot write Octave functions')

    # Handle matlab objects.
    if isinstance(data, MatlabObject):
        view = data.view(np.ndarray)
        out = MatlabObject(data, data.classname)
        for name in out.dtype.names:
            out[name] = _encode(view[name], ctf)
        return out

    # Handle pandas series and dataframes
    if isinstance(data, (DataFrame, Series)):
        return _encode(data.values, ctf)

    # Extract and encode values from dict-like objects.
    if isinstance(data, dict):
        out = dict()
        for (key, value) in data.items():
            out[key] = _encode(value, ctf)
        return out

    # Send None as nan.
    if data is None:
        return np.NaN

    # Sets are treated like lists.
    if isinstance(data, set):
        return _encode(list(data), ctf)

    # Lists can be interpreted as numeric arrays or cell arrays.
    if isinstance(data, list):
        if _is_simple_numeric(data):
            return _encode(np.array(data), ctf)
        return _encode(tuple(data), ctf)

    # Tuples are handled as cells.
    if isinstance(data, tuple):
        obj = np.empty(len(data), dtype=object)
        for (i, item) in enumerate(data):
            obj[i] = _encode(item, ctf)
        return obj

    # Sparse data must be floating type.
    if isinstance(data, spmatrix):
        return data.astype(np.float64)

    # Return other data types unchanged.
    if not isinstance(data, np.ndarray):
        return data

    # Extract and encode data from object-like arrays.
    if data.dtype.kind in 'OV':
        out = np.empty(data.size, dtype=data.dtype)
        for (i, item) in enumerate(data.ravel()):
            if data.dtype.names:
                for name in data.dtype.names:
                    out[i][name] = _encode(item[name], ctf)
            else:
                out[i] = _encode(item, ctf)
        return out.reshape(data.shape)

    # Complex 128 is the highest supported by savemat.
    if data.dtype.name == 'complex256':
        return data.astype(np.complex128)

    # Convert to float if applicable.
    if ctf and data.dtype.kind in 'ui':
        return data.astype(np.float64)

    # Return standard array.
    return data