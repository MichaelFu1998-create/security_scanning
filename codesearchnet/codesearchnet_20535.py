def new_img_like(ref_niimg, data, affine=None, copy_header=False):
    """Create a new image of the same class as the reference image

    Parameters
    ----------
    ref_niimg: image
        Reference image. The new image will be of the same type.

    data: numpy array
        Data to be stored in the image

    affine: 4x4 numpy array, optional
        Transformation matrix

    copy_header: boolean, optional
        Indicated if the header of the reference image should be used to
        create the new image

    Returns
    -------
    new_img: image
        A loaded image with the same type (and header) as the reference image.
    """
    # Hand-written loading code to avoid too much memory consumption
    if not (hasattr(ref_niimg, 'get_data')
              and hasattr(ref_niimg,'get_affine')):
        if isinstance(ref_niimg, _basestring):
            ref_niimg = nib.load(ref_niimg)
        elif operator.isSequenceType(ref_niimg):
            ref_niimg = nib.load(ref_niimg[0])
        else:
            raise TypeError(('The reference image should be a niimg, %r '
                            'was passed') % ref_niimg )

    if affine is None:
        affine = ref_niimg.get_affine()
    if data.dtype == bool:
        default_dtype = np.int8
        if (LooseVersion(nib.__version__) >= LooseVersion('1.2.0') and
                isinstance(ref_niimg, nib.freesurfer.mghformat.MGHImage)):
            default_dtype = np.uint8
        data = as_ndarray(data, dtype=default_dtype)
    header = None
    if copy_header:
        header = copy.copy(ref_niimg.get_header())
        header['scl_slope'] = 0.
        header['scl_inter'] = 0.
        header['glmax'] = 0.
        header['cal_max'] = np.max(data) if data.size > 0 else 0.
        header['cal_max'] = np.min(data) if data.size > 0 else 0.
    return ref_niimg.__class__(data, affine, header=header)