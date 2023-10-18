def extract_datasets(h5file, h5path='/'):
    """ Return all dataset contents from h5path group in h5file in an OrderedDict.

    Parameters
    ----------
    h5file: h5py.File
        HDF5 file object

    h5path: str
        HDF5 group path to read datasets from

    Returns
    -------
    datasets: OrderedDict
        Dict with variables contained in file_path/h5path
    """
    if isinstance(h5file, str):
        _h5file = h5py.File(h5file, mode='r')
    else:
        _h5file = h5file

    _datasets = get_datasets(_h5file, h5path)
    datasets  = OrderedDict()
    try:
        for ds in _datasets:
            datasets[ds.name.split('/')[-1]] = ds[:]
    except:
        raise RuntimeError('Error reading datasets in {}/{}.'.format(_h5file.filename, h5path))
    finally:
        if isinstance(h5file, str):
            _h5file.close()

    return datasets