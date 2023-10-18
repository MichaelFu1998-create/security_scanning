def open_volume_file(filepath):
    """Open a volumetric file using the tools following the file extension.

    Parameters
    ----------
    filepath: str
        Path to a volume file

    Returns
    -------
    volume_data: np.ndarray
        Volume data

    pixdim: 1xN np.ndarray
        Vector with the description of the voxels physical size (usually in mm) for each volume dimension.

    Raises
    ------
    IOError
        In case the file is not found.
    """
    # check if the file exists
    if not op.exists(filepath):
        raise IOError('Could not find file {}.'.format(filepath))

    # define helper functions
    def open_nifti_file(filepath):
        return NiftiImage(filepath)

    def open_mhd_file(filepath):
        return MedicalImage(filepath)
        vol_data, hdr_data = load_raw_data_with_mhd(filepath)
        # TODO: convert vol_data and hdr_data into MedicalImage
        return vol_data, hdr_data

    def open_mha_file(filepath):
        raise NotImplementedError('This function has not been implemented yet.')

    # generic loader function
    def _load_file(filepath, loader):
        return loader(filepath)

    # file_extension -> file loader function
    filext_loader = {
                    'nii': open_nifti_file,
                    'mhd': open_mhd_file,
                    'mha': open_mha_file,
                    }

    # get extension of the `filepath`
    ext = get_extension(filepath)

    # find the loader from `ext`
    loader = None
    for e in filext_loader:
        if ext in e:
            loader = filext_loader[e]

    if loader is None:
        raise ValueError('Could not find a loader for file {}.'.format(filepath))

    return _load_file(filepath, loader)