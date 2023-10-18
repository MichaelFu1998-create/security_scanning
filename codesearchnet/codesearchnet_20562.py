def _check_medimg(image, make_it_3d=True):
    """Check that image is a proper img. Turn filenames into objects.

    Parameters
    ----------
    image: img-like object or str
        Can either be:
        - a file path to a medical image file, e.g. NifTI, .mhd/raw, .mha
        - any object with get_data() method and affine & header attributes, e.g., nibabel.Nifti1Image.
        - a Numpy array, which will be wrapped by a nibabel.Nifti2Image class with an `eye` affine.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

    make_it_3d: boolean, optional
        If True, check if the image is a 3D image and raise an error if not.

    Returns
    -------
    result: nifti-like
       result can be nibabel.Nifti1Image or the input, as-is. It is guaranteed
       that the returned object has get_data() and get_affine() methods.
    """
    if isinstance(image, string_types):
        # a filename, load it
        img = open_volume_file(image)

        if make_it_3d:
            img = _make_it_3d(img)

        return img

    elif isinstance(image, np.array):
        return nib.Nifti2Image(image, affine=np.eye(image.ndim + 1))

    elif isinstance(image, nib.Nifti1Image) or is_img(image):
        return image

    else:
        raise TypeError('Data given cannot be converted to a medical image'
                        ' image: this object -"{}"- does not have'
                        ' get_data or get_affine methods'.format(type(image)))