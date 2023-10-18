def _smooth_data_array(arr, affine, fwhm, copy=True):
    """Smooth images with a a Gaussian filter.

    Apply a Gaussian filter along the three first dimensions of arr.

    Parameters
    ----------
    arr: numpy.ndarray
        3D or 4D array, with image number as last dimension.

    affine: numpy.ndarray
        Image affine transformation matrix for image.

    fwhm: scalar, numpy.ndarray
        Smoothing kernel size, as Full-Width at Half Maximum (FWHM) in millimeters.
        If a scalar is given, kernel width is identical on all three directions.
        A numpy.ndarray must have 3 elements, giving the FWHM along each axis.

    copy: bool
        if True, will make a copy of the input array. Otherwise will directly smooth the input array.

    Returns
    -------
    smooth_arr: numpy.ndarray
    """

    if arr.dtype.kind == 'i':
        if arr.dtype == np.int64:
            arr = arr.astype(np.float64)
        else:
            arr = arr.astype(np.float32)
    if copy:
        arr = arr.copy()

    # Zeroe possible NaNs and Inf in the image.
    arr[np.logical_not(np.isfinite(arr))] = 0

    try:
        # Keep the 3D part of the affine.
        affine = affine[:3, :3]

        # Convert from FWHM in mm to a sigma.
        fwhm_sigma_ratio = np.sqrt(8 * np.log(2))
        vox_size         = np.sqrt(np.sum(affine ** 2, axis=0))
        sigma            = fwhm / (fwhm_sigma_ratio * vox_size)
        for n, s in enumerate(sigma):
            ndimage.gaussian_filter1d(arr, s, output=arr, axis=n)
    except:
        raise ValueError('Error smoothing the array.')
    else:
        return arr