def get_img_info(image):
    """Return the header and affine matrix from a Nifti file.

    Parameters
    ----------
    image: img-like object or str
        Can either be:
        - a file path to a Nifti image
        - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

    Returns
    -------
    hdr, aff
    """
    try:
        img = check_img(image)
    except Exception as exc:
        raise Exception('Error reading file {0}.'.format(repr_imgs(image))) from exc
    else:
        return img.get_header(), img.get_affine()