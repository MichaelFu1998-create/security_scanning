def get_img_data(image, copy=True):
    """Return the voxel matrix of the Nifti file.
    If safe_mode will make a copy of the img before returning the data, so the input image is not modified.

    Parameters
    ----------
    image: img-like object or str
        Can either be:
        - a file path to a Nifti image
        - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

    copy: bool
    If safe_mode will make a copy of the img before returning the data, so the input image is not modified.

    Returns
    -------
    array_like
    """
    try:
        img = check_img(image)
        if copy:
            return get_data(img)
        else:
            return img.get_data()
    except Exception as exc:
        raise Exception('Error when reading file {0}.'.format(repr_imgs(image))) from exc