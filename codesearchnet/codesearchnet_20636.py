def spatialimg_to_hdfgroup(h5group, spatial_img):
    """Saves a Nifti1Image into an HDF5 group.

    Parameters
    ----------
    h5group: h5py Group
        Output HDF5 file path

    spatial_img: nibabel SpatialImage
        Image to be saved

    h5path: str
        HDF5 group path where the image data will be saved.
        Datasets will be created inside the given group path:
        'data', 'extra', 'affine', the header information will
        be set as attributes of the 'data' dataset.

    """
    try:
        h5group['data']   = spatial_img.get_data()
        h5group['affine'] = spatial_img.get_affine()

        if hasattr(h5group, 'get_extra'):
            h5group['extra'] = spatial_img.get_extra()

        hdr = spatial_img.get_header()
        for k in list(hdr.keys()):
            h5group['data'].attrs[k] = hdr[k]

    except ValueError as ve:
        raise Exception('Error creating group ' + h5group.name) from ve