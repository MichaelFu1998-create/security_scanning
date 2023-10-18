def load_raw_data_with_mhd(filename):
    """Return a dictionary of meta data from meta header file.

    Parameters
    ----------
    filename: str
        Path to a .mhd file

    Returns
    -------
    data: numpy.ndarray
        n-dimensional image data array.

    meta_dict: dict
        A dictionary with the .mhd header content.
    """
    meta_dict = _read_meta_header(filename)
    dim       = int(meta_dict['NDims'])

    assert (meta_dict['ElementType'] in MHD_TO_NUMPY_TYPE)

    arr = [int(i) for i in meta_dict['DimSize'].split()]
    volume = reduce(lambda x, y: x*y, arr[0:dim-1], 1)

    pwd       = op.dirname(filename)
    raw_file  = meta_dict['ElementDataFile']
    data_file = op.join(pwd, raw_file)

    ndtype    = MHD_TO_NUMPY_TYPE[meta_dict['ElementType']]
    arrtype   = NDARRAY_TO_ARRAY_TYPE[ndtype]

    with open(data_file, 'rb') as fid:
        binvalues = array.array(arrtype)
        binvalues.fromfile(fid, volume*arr[dim-1])

    data = np.array  (binvalues, ndtype)
    data = np.reshape(data, (arr[dim-1], volume))

    if dim >= 3:
        # Begin 3D fix
        dimensions = [int(i) for i in meta_dict['DimSize'].split()]
        # dimensions.reverse() ??
        data       = data.reshape(dimensions)
        # End 3D fix

    return data, meta_dict