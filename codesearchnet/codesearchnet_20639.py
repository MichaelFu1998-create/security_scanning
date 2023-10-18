def hdfgroup_to_nifti1image(h5group):
    """Returns a nibabel Nifti1Image from a HDF5 group datasets

    Parameters
    ----------
    h5group: h5py.Group
        HDF5 group

    Returns
    -------
    nibabel Nifti1Image
    """
    try:
        data   = h5group['data'][:]
        affine = h5group['affine'][:]

        extra = None
        if 'extra' in h5group:
            extra = h5group['extra'][:]

        header = get_nifti1hdr_from_h5attrs(h5group['data'].attrs)

        img = nib.Nifti1Image(data, affine, header=header, extra=extra)

        return img

    except KeyError as ke:
        raise Exception('Could not read Nifti1Image datasets from ' + h5group.name) from ke