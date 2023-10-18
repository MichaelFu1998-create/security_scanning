def save_variables_to_hdf5(file_path, variables, mode='w', h5path='/'):
    """
    Parameters
    ----------
    file_path: str

    variables: dict
        Dictionary with objects. Object name -> object

    mode: str
        HDF5 file access mode
        See h5py documentation for details.
        r   Readonly, file must exist
        r+  Read/write, file must exist
        w   Create file, truncate if exists
        w-  Create file, fail if exists
        a   Read/write if exists, create otherwise (default)

    Notes
    -----
    It is recommended to use numpy arrays as objects.
    List or tuples of strings won't work, convert them into numpy.arrays before.
    """
    if not isinstance(variables, dict):
        raise ValueError('Expected `variables` to be a dict, got a {}.'.format(type(variables)))

    if not variables:
        raise ValueError('Expected `variables` to be a non-empty dict.')

    h5file  = h5py.File(file_path, mode=mode)
    h5group = h5file.require_group(h5path)

    for vn in variables:
        data = variables[vn]

        # fix for string numpy arrays
        if hasattr(data, 'dtype') and (data.dtype.type is np.string_ or data.dtype.type is np.unicode_):
            dt   = h5py.special_dtype(vlen=str)
            data = data.astype(dt)

        if isinstance(data, dict):
            for key in data:
                #h5group.create_dataset(str(key))
                #import ipdb
                #ipdb.set_trace()
                h5group[str(key)] = data[key]

        elif isinstance(data, list):
            for idx, item in enumerate(data):
                #h5group.create_dataset(str(idx))
                h5group[str(idx)] = item
        else:
            h5group[vn] = data

    h5file.close()