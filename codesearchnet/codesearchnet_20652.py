def _check_xl_path(xl_path: str):
    """ Return the expanded absolute path of `xl_path` if
    if exists and 'xlrd' or 'openpyxl' depending on
    which module should be used for the Excel file in `xl_path`.

    Parameters
    ----------
    xl_path: str
        Path to an Excel file

    Returns
    -------
    xl_path: str
        User expanded and absolute path to `xl_path`

    module: str
        The name of the module you should use to process the
        Excel file.
        Choices: 'xlrd', 'pyopenxl'

    Raises
    ------
    IOError
        If the file does not exist

    RuntimError
        If a suitable reader for xl_path is not found
    """
    xl_path = op.abspath(op.expanduser(xl_path))

    if not op.isfile(xl_path):
        raise IOError("Could not find file in {}.".format(xl_path))

    return xl_path, _use_openpyxl_or_xlrf(xl_path)