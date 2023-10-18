def apply_mask_4d(image, mask_img):  # , smooth_mm=None, remove_nans=True):
    """Read a Nifti file nii_file and a mask Nifti file.
    Extract the signals in nii_file that are within the mask, the mask indices
    and the mask shape.

    Parameters
    ----------
    image: img-like object or boyle.nifti.NeuroImage or str
        Can either be:
        - a file path to a Nifti image
        - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

    mask_img: img-like object or boyle.nifti.NeuroImage or str
        3D mask array: True where a voxel should be used.
        See img description.

    smooth_mm: float #TBD
        (optional) The size in mm of the FWHM Gaussian kernel to smooth the signal.
        If True, remove_nans is True.

    remove_nans: bool #TBD
        If remove_nans is True (default), the non-finite values (NaNs and
        infs) found in the images will be replaced by zeros.

    Returns
    -------
    session_series, mask_data

    session_series: numpy.ndarray
        2D array of series with shape (voxel number, image number)

    Note
    ----
    nii_file and mask_file must have the same shape.

    Raises
    ------
    FileNotFound, NiftiFilesNotCompatible
    """
    img  = check_img(image)
    mask = check_img(mask_img)
    check_img_compatibility(img, mask, only_check_3d=True)

    vol = get_data(img)
    series, mask_data = _apply_mask_to_4d_data(vol, mask)
    return series, mask_data