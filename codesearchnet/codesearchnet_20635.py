def save_niigz(filepath, vol, header=None, affine=None):
    """Saves a volume into a Nifti (.nii.gz) file.

    Parameters
    ----------
    vol: Numpy 3D or 4D array
        Volume with the data to be saved.

    file_path: string
        Output file name path

    affine: (optional) 4x4 Numpy array
        Array with the affine transform of the file.
        This is needed if vol is a np.ndarray.

    header: (optional) nibabel.nifti1.Nifti1Header, optional
        Header for the file, optional but recommended.
        This is needed if vol is a np.ndarray.

    Note
    ----
    affine and header only work for numpy volumes.
    """
    # delayed import because could not install nipy on Python 3 on OSX
    we_have_nipy = False
    try:
        import nipy.core.image as     niim
        from   nipy            import save_image
    except:
        pass
    else:
        we_have_nipy = True

    if isinstance(vol, np.ndarray):
        log.debug('Saving numpy nifti file: {}.'.format(filepath))
        ni = nib.Nifti1Image(vol, affine, header)
        nib.save(ni, filepath)

    elif isinstance(vol, nib.Nifti1Image):
        log.debug('Saving nibabel nifti file: {}.'.format(filepath))
        nib.save(vol, filepath)

    elif we_have_nipy and isinstance(vol, niim.Image):
        log.debug('Saving nipy nifti file: {}.'.format(filepath))
        save_image(vol, filepath)

    #elif isinstance(vol, NeuroImage):
    #    log.debug('Saving boyle.NeuroImage nifti file: {}.'.format(filepath))
    #    nib.save(vol.img, filepath)

    else:
        raise ValueError('Could not recognise input vol filetype. Got: {}.'.format(repr_imgs(vol)))