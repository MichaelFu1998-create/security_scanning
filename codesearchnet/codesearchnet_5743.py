def _create_file_if_needed(filename):
    """Creates the an empty file if it does not already exist.

    Returns:
        True if the file was created, False otherwise.
    """
    if os.path.exists(filename):
        return False
    else:
        # Equivalent to "touch".
        open(filename, 'a+b').close()
        logger.info('Credential file {0} created'.format(filename))
        return True