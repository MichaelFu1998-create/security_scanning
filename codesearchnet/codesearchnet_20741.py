def load_mask_data(image, allow_empty=True):
    """Load a Nifti mask volume and return its data matrix as boolean and affine.

    Parameters
    ----------
    image: img-like object or boyle.nifti.NeuroImage or str
        Can either be:
        - a file path to a Nifti image
        - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

    allow_empty: boolean, optional
        Allow loading an empty mask (full of 0 values)

    Returns
    -------
    numpy.ndarray with dtype==bool, numpy.ndarray of affine transformation
    """
    mask = load_mask(image, allow_empty=allow_empty)
    return get_img_data(mask), mask.get_affine()