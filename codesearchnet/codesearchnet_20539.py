def _get_node_names(h5file, h5path='/', node_type=h5py.Dataset):
    """Return the node of type node_type names within h5path of h5file.

    Parameters
    ----------
    h5file: h5py.File
        HDF5 file object

    h5path: str
        HDF5 group path to get the group names from

    node_type: h5py object type
        HDF5 object type

    Returns
    -------
    names: list of str
        List of names
    """
    if isinstance(h5file, str):
        _h5file = get_h5file(h5file, mode='r')
    else:
        _h5file = h5file

    if not h5path.startswith('/'):
        h5path = '/' + h5path

    names = []
    try:
        h5group = _h5file.require_group(h5path)

        for node in _hdf5_walk(h5group, node_type=node_type):
            names.append(node.name)
    except:
        raise RuntimeError('Error getting node names from {}/{}.'.format(_h5file.filename, h5path))
    finally:
        if isinstance(h5file, str):
            _h5file.close()

    return names