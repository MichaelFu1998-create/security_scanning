def is_dicom_file(filepath):
    """
    Tries to read the file using dicom.read_file,
    if the file exists and dicom.read_file does not raise
    and Exception returns True. False otherwise.

    :param filepath: str
     Path to DICOM file

    :return: bool
    """
    if not os.path.exists(filepath):
        raise IOError('File {} not found.'.format(filepath))

    filename = os.path.basename(filepath)
    if filename == 'DICOMDIR':
        return False

    try:
        _ = dicom.read_file(filepath)
    except Exception as exc:
        log.debug('Checking if {0} was a DICOM, but returned '
                  'False.'.format(filepath))
        return False

    return True