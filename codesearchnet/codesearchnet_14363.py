def setup(template, version=None):
    """Sets up a new project from a template

    Note that the `temple.constants.TEMPLE_ENV_VAR` is set to 'setup' during the duration
    of this function.

    Args:
        template (str): The git SSH path to a template
        version (str, optional): The version of the template to use when updating. Defaults
            to the latest version
    """
    temple.check.is_git_ssh_path(template)
    temple.check.not_in_git_repo()

    repo_path = temple.utils.get_repo_path(template)
    msg = (
        'You will be prompted for the parameters of your new project.'
        ' Please read the docs at https://github.com/{} before entering parameters.'
    ).format(repo_path)
    print(msg)

    cc_repo_dir, config = temple.utils.get_cookiecutter_config(template, version=version)

    if not version:
        with temple.utils.cd(cc_repo_dir):
            ret = temple.utils.shell('git rev-parse HEAD', stdout=subprocess.PIPE)
            version = ret.stdout.decode('utf-8').strip()

    _generate_files(repo_dir=cc_repo_dir, config=config, template=template, version=version)