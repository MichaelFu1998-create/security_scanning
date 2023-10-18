def get_3D_from_4D(image, vol_idx=0):
    """Pick one 3D volume from a 4D nifti image file

    Parameters
    ----------
    image: img-like object or str
        Volume defining different ROIs.
        Can either be:
        - a file path to a Nifti image
        - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

    vol_idx: int
        Index of the 3D volume to be extracted from the 4D volume.

    Returns
    -------
    vol, hdr, aff
        The data array, the image header and the affine transform matrix.
    """
    img      = check_img(image)
    hdr, aff = get_img_info(img)

    if len(img.shape) != 4:
        raise AttributeError('Volume in {} does not have 4 dimensions.'.format(repr_imgs(img)))

    if not 0 <= vol_idx < img.shape[3]:
        raise IndexError('IndexError: 4th dimension in volume {} has {} volumes, '
                         'not {}.'.format(repr_imgs(img), img.shape[3], vol_idx))

    img_data = img.get_data()
    new_vol  = img_data[:, :, :, vol_idx].copy()

    hdr.set_data_shape(hdr.get_data_shape()[:3])

    return new_vol, hdr, aff