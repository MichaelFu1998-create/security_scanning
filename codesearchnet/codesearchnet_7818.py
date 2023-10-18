def validate_input_file(input_filepath):
    '''Input file validation function. Checks that file exists and can be
    processed by SoX.

    Parameters
    ----------
    input_filepath : str
        The input filepath.

    '''
    if not os.path.exists(input_filepath):
        raise IOError(
            "input_filepath {} does not exist.".format(input_filepath)
        )
    ext = file_extension(input_filepath)
    if ext not in VALID_FORMATS:
        logger.info("Valid formats: %s", " ".join(VALID_FORMATS))
        logger.warning(
            "This install of SoX cannot process .{} files.".format(ext)
        )