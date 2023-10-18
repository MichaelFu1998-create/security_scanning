def validate_output_file(output_filepath):
    '''Output file validation function. Checks that file can be written, and
    has a valid file extension. Throws a warning if the path already exists,
    as it will be overwritten on build.

    Parameters
    ----------
    output_filepath : str
        The output filepath.

    Returns:
    --------
    output_filepath : str
        The output filepath.

    '''

    nowrite_conditions = [
        bool(os.path.dirname(output_filepath)) or\
            not os.access(os.getcwd(), os.W_OK),
        not os.access(os.path.dirname(output_filepath), os.W_OK)]

    if all(nowrite_conditions):
        raise IOError(
            "SoX cannot write to output_filepath {}".format(output_filepath)
        )

    ext = file_extension(output_filepath)
    if ext not in VALID_FORMATS:
        logger.info("Valid formats: %s", " ".join(VALID_FORMATS))
        logger.warning(
            "This install of SoX cannot process .{} files.".format(ext)
        )

    if os.path.exists(output_filepath):
        logger.warning(
            'output_file: %s already exists and will be overwritten on build',
            output_filepath
        )