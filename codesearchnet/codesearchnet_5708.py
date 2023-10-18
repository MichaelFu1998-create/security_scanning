def save_to_well_known_file(credentials, well_known_file=None):
    """Save the provided GoogleCredentials to the well known file.

    Args:
        credentials: the credentials to be saved to the well known file;
                     it should be an instance of GoogleCredentials
        well_known_file: the name of the file where the credentials are to be
                         saved; this parameter is supposed to be used for
                         testing only
    """
    # TODO(orestica): move this method to tools.py
    # once the argparse import gets fixed (it is not present in Python 2.6)

    if well_known_file is None:
        well_known_file = _get_well_known_file()

    config_dir = os.path.dirname(well_known_file)
    if not os.path.isdir(config_dir):
        raise OSError(
            'Config directory does not exist: {0}'.format(config_dir))

    credentials_data = credentials.serialization_data
    _save_private_file(well_known_file, credentials_data)