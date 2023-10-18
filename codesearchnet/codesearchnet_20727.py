def call_dcm2nii(work_dir, arguments=''):
    """Converts all DICOM files within `work_dir` into one or more
    NifTi files by calling dcm2nii on this folder.

    Parameters
    ----------
    work_dir: str
        Path to the folder that contain the DICOM files

    arguments: str
        String containing all the flag arguments for `dcm2nii` CLI.

    Returns
    -------
    sys_code: int
        dcm2nii execution return code
    """
    if not op.exists(work_dir):
        raise IOError('Folder {} not found.'.format(work_dir))

    cmd_line = 'dcm2nii {0} "{1}"'.format(arguments, work_dir)
    log.info(cmd_line)
    return subprocess.check_call(cmd_line, shell=True)