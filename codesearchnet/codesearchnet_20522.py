def smooth_img(imgs, fwhm, **kwargs):
    """Smooth images by applying a Gaussian filter.
    Apply a Gaussian filter along the three first dimensions of arr.
    In all cases, non-finite values in input image are replaced by zeros.

    This is copied and slightly modified from nilearn:
    https://github.com/nilearn/nilearn/blob/master/nilearn/image/image.py
    Added the **kwargs argument.

    Parameters
    ==========
    imgs: Niimg-like object or iterable of Niimg-like objects
        See http://nilearn.github.io/manipulating_images/manipulating_images.html#niimg.
        Image(s) to smooth.
    fwhm: scalar, numpy.ndarray, 'fast' or None
        Smoothing strength, as a Full-Width at Half Maximum, in millimeters.
        If a scalar is given, width is identical on all three directions.
        A numpy.ndarray must have 3 elements, giving the FWHM along each axis.
        If fwhm == 'fast', a fast smoothing will be performed with
        a filter [0.2, 1, 0.2] in each direction and a normalisation
        to preserve the scale.
        If fwhm is None, no filtering is performed (useful when just removal
        of non-finite values is needed)
    Returns
    =======
    filtered_img: nibabel.Nifti1Image or list of.
        Input image, filtered. If imgs is an iterable, then filtered_img is a
        list.
    """

    # Use hasattr() instead of isinstance to workaround a Python 2.6/2.7 bug
    # See http://bugs.python.org/issue7624
    if hasattr(imgs, "__iter__") \
       and not isinstance(imgs, string_types):
        single_img = False
    else:
        single_img = True
        imgs = [imgs]

    ret = []
    for img in imgs:
        img = check_niimg(img)
        affine = img.get_affine()
        filtered = _smooth_array(img.get_data(), affine, fwhm=fwhm,
                                 ensure_finite=True, copy=True, **kwargs)
        ret.append(new_img_like(img, filtered, affine, copy_header=True))

    if single_img:
        return ret[0]
    else:
        return ret