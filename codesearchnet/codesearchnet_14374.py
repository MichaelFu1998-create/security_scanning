def is_temple_project():
    """Raises `InvalidTempleProjectError` if repository is not a temple project"""
    if not os.path.exists(temple.constants.TEMPLE_CONFIG_FILE):
        msg = 'No {} file found in repository.'.format(temple.constants.TEMPLE_CONFIG_FILE)
        raise temple.exceptions.InvalidTempleProjectError(msg)