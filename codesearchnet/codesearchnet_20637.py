def spatialimg_to_hdfpath(file_path, spatial_img, h5path=None, append=True):
    """Saves a Nifti1Image into an HDF5 file.

    Parameters
    ----------
    file_path: string
        Output HDF5 file path

    spatial_img: nibabel SpatialImage
        Image to be saved

    h5path: string
        HDF5 group path where the image data will be saved.
        Datasets will be created inside the given group path:
        'data', 'extra', 'affine', the header information will
        be set as attributes of the 'data' dataset.
        Default: '/img'

    append: bool
        True if you don't want to erase the content of the file
        if it already exists, False otherwise.

    Note
    ----
    HDF5 open modes
    >>> 'r' Readonly, file must exist
    >>> 'r+' Read/write, file must exist
    >>> 'w' Create file, truncate if exists
    >>> 'w-' Create file, fail if exists
    >>> 'a' Read/write if exists, create otherwise (default)

    """
    if h5path is None:
        h5path = '/img'

    mode = 'w'
    if os.path.exists(file_path):
        if append:
            mode = 'a'

    with h5py.File(file_path, mode) as f:
        try:
            h5img = f.create_group(h5path)
            spatialimg_to_hdfgroup(h5img, spatial_img)

        except ValueError as ve:
            raise Exception('Error creating group ' + h5path) from ve