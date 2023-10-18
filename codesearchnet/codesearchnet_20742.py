def union_mask(filelist):
    """
    Creates a binarised mask with the union of the files in filelist.

    Parameters
    ----------
    filelist: list of img-like object or boyle.nifti.NeuroImage or str
        List of paths to the volume files containing the ROIs.
        Can either be:
        - a file path to a Nifti image
        - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

    Returns
    -------
    ndarray of bools
        Mask volume

    Raises
    ------
    ValueError
    """
    firstimg = check_img(filelist[0])
    mask     = np.zeros_like(firstimg.get_data())

    # create space for all features and read from subjects
    try:
        for volf in filelist:
            roiimg = check_img(volf)
            check_img_compatibility(firstimg, roiimg)
            mask  += get_img_data(roiimg)
    except Exception as exc:
        raise ValueError('Error joining mask {} and {}.'.format(repr_imgs(firstimg), repr_imgs(volf))) from exc
    else:
        return as_ndarray(mask > 0, dtype=bool)