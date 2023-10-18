def check_img_compatibility(one_img, another_img, only_check_3d=False):
    """Return true if one_img and another_img have the same shape.
    False otherwise.
    If both are nibabel.Nifti1Image will also check for affine matrices.

    Parameters
    ----------
    one_img: nibabel.Nifti1Image or np.ndarray

    another_img: nibabel.Nifti1Image  or np.ndarray

    only_check_3d: bool
        If True will check only the 3D part of the affine matrices when they have more dimensions.

    Raises
    ------
    NiftiFilesNotCompatible
    """
    nd_to_check = None
    if only_check_3d:
        nd_to_check = 3

    if hasattr(one_img, 'shape') and hasattr(another_img, 'shape'):
        if not have_same_shape(one_img, another_img, nd_to_check=nd_to_check):
            msg = 'Shape of the first image: \n{}\n is different from second one: \n{}'.format(one_img.shape,
                                                                                               another_img.shape)
            raise NiftiFilesNotCompatible(repr_imgs(one_img), repr_imgs(another_img), message=msg)

    if hasattr(one_img, 'get_affine') and hasattr(another_img, 'get_affine'):
        if not have_same_affine(one_img, another_img, only_check_3d=only_check_3d):
            msg = 'Affine matrix of the first image: \n{}\n is different ' \
                  'from second one:\n{}'.format(one_img.get_affine(), another_img.get_affine())
            raise NiftiFilesNotCompatible(repr_imgs(one_img), repr_imgs(another_img), message=msg)