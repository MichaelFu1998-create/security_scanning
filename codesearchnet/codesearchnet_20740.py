def load_mask(image, allow_empty=True):
    """Load a Nifti mask volume.

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
    nibabel.Nifti1Image with boolean data.
    """
    img    = check_img(image, make_it_3d=True)
    values = np.unique(img.get_data())

    if len(values) == 1:
        # We accept a single value if it is not 0 (full true mask).
        if values[0] == 0 and not allow_empty:
            raise ValueError('Given mask is invalid because it masks all data')

    elif len(values) == 2:
        # If there are 2 different values, one of them must be 0 (background)
        if 0 not in values:
            raise ValueError('Background of the mask must be represented with 0.'
                             ' Given mask contains: {}.'.format(values))

    elif len(values) != 2:
        # If there are more than 2 values, the mask is invalid
            raise ValueError('Given mask is not made of 2 values: {}. '
                             'Cannot interpret as true or false'.format(values))

    return nib.Nifti1Image(as_ndarray(get_img_data(img), dtype=bool), img.get_affine(), img.get_header())