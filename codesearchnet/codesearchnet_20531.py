def load_nipy_img(nii_file):
    """Read a Nifti file and return as nipy.Image

    Parameters
    ----------
    param nii_file: str
        Nifti file path

    Returns
    -------
    nipy.Image
    """
    # delayed import because could not install nipy on Python 3 on OSX
    import nipy

    if not os.path.exists(nii_file):
        raise FileNotFound(nii_file)

    try:
        return nipy.load_image(nii_file)
    except Exception as exc:
        raise Exception('Reading file {0}.'.format(repr_imgs(nii_file))) from exc