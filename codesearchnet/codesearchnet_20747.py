def niftilist_mask_to_array(img_filelist, mask_file=None, outdtype=None):
    """From the list of absolute paths to nifti files, creates a Numpy array
    with the masked data.

    Parameters
    ----------
    img_filelist: list of str
        List of absolute file paths to nifti files. All nifti files must have
        the same shape.

    mask_file: str
        Path to a Nifti mask file.
        Should be the same shape as the files in nii_filelist.

    outdtype: dtype
        Type of the elements of the array, if not set will obtain the dtype from
        the first nifti file.

    Returns
    -------
    outmat:
        Numpy array with shape N x prod(vol.shape) containing the N files as flat vectors.

    mask_indices:
        Tuple with the 3D spatial indices of the masking voxels, for reshaping
        with vol_shape and remapping.

    vol_shape:
        Tuple with shape of the volumes, for reshaping.

    """
    img = check_img(img_filelist[0])
    if not outdtype:
        outdtype = img.dtype

    mask_data, _ = load_mask_data(mask_file)
    indices      = np.where      (mask_data)

    mask = check_img(mask_file)

    outmat = np.zeros((len(img_filelist), np.count_nonzero(mask_data)),
                      dtype=outdtype)

    for i, img_item in enumerate(img_filelist):
        img = check_img(img_item)
        if not are_compatible_imgs(img, mask):
            raise NiftiFilesNotCompatible(repr_imgs(img), repr_imgs(mask_file))

        vol = get_img_data(img)
        outmat[i, :] = vol[indices]

    return outmat, mask_data