def get_h5file(file_path, mode='r'):
    """ Return the h5py.File given its file path.

    Parameters
    ----------
    file_path: string
        HDF5 file path

    mode: string
        r   Readonly, file must exist
        r+  Read/write, file must exist
        w   Create file, truncate if exists
        w-  Create file, fail if exists
        a   Read/write if exists, create otherwise (default)

    Returns
    -------
    h5file: h5py.File
    """
    if not op.exists(file_path):
        raise IOError('Could not find file {}.'.format(file_path))

    try:
        h5file = h5py.File(file_path, mode=mode)
    except:
        raise
    else:
        return h5file