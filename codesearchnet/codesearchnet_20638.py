def hdfpath_to_nifti1image(file_path, h5path):
    """Returns a nibabel Nifti1Image from a HDF5 group datasets

    Parameters
    ----------
    file_path: string
        HDF5 file path

    h5path:
        HDF5 group path in file_path

    Returns
    -------
        nibabel Nifti1Image
    """
    with h5py.File(file_path, 'r') as f:
        return hdfgroup_to_nifti1image(f[h5path])