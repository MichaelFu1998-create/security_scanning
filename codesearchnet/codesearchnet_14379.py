def up_to_date(version=None):
    """Checks if a temple project is up to date with the repo

    Note that the `temple.constants.TEMPLE_ENV_VAR` is set to 'update' for the duration of this
    function.

    Args:
        version (str, optional): Update against this git SHA or branch of the template

    Returns:
        boolean: True if up to date with ``version`` (or latest version), False otherwise

    Raises:
        `NotInGitRepoError`: When running outside of a git repo
        `InvalidTempleProjectError`: When not inside a valid temple repository
    """
    temple.check.in_git_repo()
    temple.check.is_temple_project()

    temple_config = temple.utils.read_temple_config()
    old_template_version = temple_config['_version']
    new_template_version = version or _get_latest_template_version(temple_config['_template'])

    return new_template_version == old_template_version