def _make_it_3d(img):
    """Enforce that img is a 3D img-like object, if it is not, raise a TypeError.
    i.e., remove dimensions of size 1.

    Parameters
    ----------
    img: img-like object

    Returns
    -------
    3D img-like object
    """
    shape = get_shape(img)
    if len(shape) == 3:
        return img

    elif (len(shape) == 4 and shape[3] == 1):
        # "squeeze" the image.
        try:
            data   = get_data(img)
            affine = img.get_affine()
            img    = nib.Nifti1Image(data[:, :, :, 0], affine)
        except Exception as exc:
            raise Exception("Error making image '{}' a 3D volume file.".format(img)) from exc
        else:
            return img
    else:
        raise TypeError("A 3D image is expected, but an image with a shape of {} was given.".format(shape))