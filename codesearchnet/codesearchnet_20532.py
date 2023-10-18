def niftilist_to_array(img_filelist, outdtype=None):
    """
    From the list of absolute paths to nifti files, creates a Numpy array
    with the data.

    Parameters
    ----------
    img_filelist:  list of str
        List of absolute file paths to nifti files. All nifti files must have
        the same shape.

    outdtype: dtype
        Type of the elements of the array, if not set will obtain the dtype from
        the first nifti file.

    Returns
    -------
    outmat: Numpy array with shape N x prod(vol.shape)
            containing the N files as flat vectors.

    vol_shape: Tuple with shape of the volumes, for reshaping.

    """
    try:
        first_img = img_filelist[0]
        vol       = get_img_data(first_img)
    except IndexError as ie:
        raise Exception('Error getting the first item of img_filelis: {}'.format(repr_imgs(img_filelist[0]))) from ie

    if not outdtype:
        outdtype = vol.dtype

    outmat = np.zeros((len(img_filelist), np.prod(vol.shape)), dtype=outdtype)

    try:
        for i, img_file in enumerate(img_filelist):
            vol = get_img_data(img_file)
            outmat[i, :] = vol.flatten()
    except Exception as exc:
        raise Exception('Error on reading file {0}.'.format(img_file)) from exc

    return outmat, vol.shape