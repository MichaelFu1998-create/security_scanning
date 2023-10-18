def smooth_imgs(images, fwhm):
    """Smooth images using a Gaussian filter.

    Apply a Gaussian filter along the three first dimensions of each image in images.
    In all cases, non-finite values in input are zeroed.

    Parameters
    ----------
    imgs: str or img-like object or iterable of img-like objects
        See boyle.nifti.read.read_img
        Image(s) to smooth.

    fwhm: scalar or numpy.ndarray
        Smoothing kernel size, as Full-Width at Half Maximum (FWHM) in millimeters.
        If a scalar is given, kernel width is identical on all three directions.
        A numpy.ndarray must have 3 elements, giving the FWHM along each axis.

    Returns
    -------
    smooth_imgs: nibabel.Nifti1Image or list of.
        Smooth input image/s.
    """
    if fwhm <= 0:
        return images

    if not isinstance(images, string_types) and hasattr(images, '__iter__'):
        only_one = False
    else:
        only_one = True
        images = [images]

    result = []
    for img in images:
        img    = check_img(img)
        affine = img.get_affine()
        smooth = _smooth_data_array(img.get_data(), affine, fwhm=fwhm, copy=True)
        result.append(nib.Nifti1Image(smooth, affine))

    if only_one:
        return result[0]
    else:
        return result