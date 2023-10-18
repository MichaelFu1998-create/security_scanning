def get_3D_coordmap(img):
    '''
    Gets a 3D CoordinateMap from img.

    Parameters
    ----------
    img: nib.Nifti1Image or nipy Image

    Returns
    -------
    nipy.core.reference.coordinate_map.CoordinateMap
    '''
    if isinstance(img, nib.Nifti1Image):
        img = nifti2nipy(img)

    if img.ndim == 4:
        from nipy.core.reference.coordinate_map import drop_io_dim
        cm = drop_io_dim(img.coordmap, 3)
    else:
        cm = img.coordmap

    return cm