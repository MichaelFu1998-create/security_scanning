def write_mhd_file(filename, data, shape=None, meta_dict=None):
    """ Write the `data` and `meta_dict` in two files with names
    that use `filename` as a prefix.

    Parameters
    ----------
    filename: str
        Path to the output file.
        This is going to be used as a preffix.
        Two files will be created, one with a '.mhd' extension
        and another with '.raw'. If `filename` has any of these already
        they will be taken into account to build the filenames.

    data: numpy.ndarray
        n-dimensional image data array.

    shape: tuple
        Tuple describing the shape of `data`
        Default: data.shape

    meta_dict: dict
        Dictionary with the fields of the metadata .mhd file
        Default: {}

    Returns
    -------
    mhd_filename: str
        Path to the .mhd file

    raw_filename: str
        Path to the .raw file
    """
    # check its extension
    ext = get_extension(filename)
    fname = op.basename(filename)
    if ext != '.mhd' or ext != '.raw':
        mhd_filename = fname + '.mhd'
        raw_filename = fname + '.raw'
    elif ext == '.mhd':
        mhd_filename = fname
        raw_filename = remove_ext(fname) + '.raw'
    elif ext == '.raw':
        mhd_filename = remove_ext(fname) + '.mhd'
        raw_filename = fname
    else:
        raise ValueError('`filename` extension {} from {} is not recognised. '
                         'Expected .mhd or .raw.'.format(ext, filename))

    # default values
    if meta_dict is None:
        meta_dict = {}

    if shape is None:
        shape = data.shape

    # prepare the default header
    meta_dict['ObjectType']             = meta_dict.get('ObjectType',             'Image')
    meta_dict['BinaryData']             = meta_dict.get('BinaryData',             'True' )
    meta_dict['BinaryDataByteOrderMSB'] = meta_dict.get('BinaryDataByteOrderMSB', 'False')
    meta_dict['ElementType']            = meta_dict.get('ElementType',            NUMPY_TO_MHD_TYPE[data.dtype.type])
    meta_dict['NDims']                  = meta_dict.get('NDims',                  str(len(shape)))
    meta_dict['DimSize']                = meta_dict.get('DimSize',                ' '.join([str(i) for i in shape]))
    meta_dict['ElementDataFile']        = meta_dict.get('ElementDataFile',        raw_filename)

    # target files
    mhd_filename = op.join(op.dirname(filename), mhd_filename)
    raw_filename = op.join(op.dirname(filename), raw_filename)

    # write the header
    write_meta_header(mhd_filename, meta_dict)

    # write the data
    dump_raw_data(raw_filename, data)

    return mhd_filename, raw_filename