def _get_well_known_file():
    """Get the well known file produced by command 'gcloud auth login'."""
    # TODO(orestica): Revisit this method once gcloud provides a better way
    # of pinpointing the exact location of the file.
    default_config_dir = os.getenv(_CLOUDSDK_CONFIG_ENV_VAR)
    if default_config_dir is None:
        if os.name == 'nt':
            try:
                default_config_dir = os.path.join(os.environ['APPDATA'],
                                                  _CLOUDSDK_CONFIG_DIRECTORY)
            except KeyError:
                # This should never happen unless someone is really
                # messing with things.
                drive = os.environ.get('SystemDrive', 'C:')
                default_config_dir = os.path.join(drive, '\\',
                                                  _CLOUDSDK_CONFIG_DIRECTORY)
        else:
            default_config_dir = os.path.join(os.path.expanduser('~'),
                                              '.config',
                                              _CLOUDSDK_CONFIG_DIRECTORY)

    return os.path.join(default_config_dir, _WELL_KNOWN_CREDENTIALS_FILE)