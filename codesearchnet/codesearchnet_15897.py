def write_file(obj, path, oned_as='row', convert_to_float=True):
    """Save a Python object to an Octave file on the given path.
    """
    data = _encode(obj, convert_to_float)
    try:
        # scipy.io.savemat is not thread-save.
        # See https://github.com/scipy/scipy/issues/7260
        with _WRITE_LOCK:
            savemat(path, data, appendmat=False, oned_as=oned_as,
                    long_field_names=True)
    except KeyError:  # pragma: no cover
        raise Exception('could not save mat file')