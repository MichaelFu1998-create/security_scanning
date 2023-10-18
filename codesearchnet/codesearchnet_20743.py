def apply_mask(image, mask_img):
    """Read a Nifti file nii_file and a mask Nifti file.
    Returns the voxels in nii_file that are within the mask, the mask indices
    and the mask shape.

    Parameters
    ----------
    image: img-like object or boyle.nifti.NeuroImage or str
        Can either be:
        - a file path to a Nifti image
        - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

    mask_img: img-like object or boyle.nifti.NeuroImage or str
        3D mask array: True where a voxel should be used.
        See img description.

    Returns
    -------
    vol[mask_indices], mask_indices

    Note
    ----
    nii_file and mask_file must have the same shape.

    Raises
    ------
    NiftiFilesNotCompatible, ValueError
    """
    img  = check_img(image)
    mask = check_img(mask_img)
    check_img_compatibility(img, mask)

    vol          = img.get_data()
    mask_data, _ = load_mask_data(mask)

    return vol[mask_data], mask_data