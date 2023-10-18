def find_all_dicom_files(root_path):
    """
    Returns a list of the dicom files within root_path

    Parameters
    ----------
    root_path: str
    Path to the directory to be recursively searched for DICOM files.

    Returns
    -------
    dicoms: set
    Set of DICOM absolute file paths
    """
    dicoms = set()

    try:
        for fpath in get_all_files(root_path):
            if is_dicom_file(fpath):
                dicoms.add(fpath)
    except IOError as ioe:
        raise IOError('Error reading file {0}.'.format(fpath)) from ioe

    return dicoms