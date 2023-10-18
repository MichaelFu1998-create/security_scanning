def have_same_affine(one_img, another_img, only_check_3d=False):
    """Return True if the affine matrix of one_img is close to the affine matrix of another_img.
    False otherwise.

    Parameters
    ----------
    one_img: nibabel.Nifti1Image

    another_img: nibabel.Nifti1Image

    only_check_3d: bool
        If True will extract only the 3D part of the affine matrices when they have more dimensions.

    Returns
    -------
    bool

    Raises
    ------
    ValueError

    """
    img1 = check_img(one_img)
    img2 = check_img(another_img)

    ndim1 = len(img1.shape)
    ndim2 = len(img2.shape)

    if ndim1 < 3:
        raise ValueError('Image {} has only {} dimensions, at least 3 dimensions is expected.'.format(repr_imgs(img1), ndim1))

    if ndim2 < 3:
        raise ValueError('Image {} has only {} dimensions, at least 3 dimensions is expected.'.format(repr_imgs(img2), ndim1))

    affine1 = img1.get_affine()
    affine2 = img2.get_affine()
    if only_check_3d:
        affine1 = affine1[:3, :3]
        affine2 = affine2[:3, :3]

    try:
        return np.allclose(affine1, affine2)
    except ValueError:
        return False
    except:
        raise