def ls(github_user, template=None):
    """Lists all temple templates and packages associated with those templates

    If ``template`` is None, returns the available templates for the configured
    Github org.

    If ``template`` is a Github path to a template, returns all projects spun
    up with that template.

    ``ls`` uses the github search API to find results.

    Note that the `temple.constants.TEMPLE_ENV_VAR` is set to 'ls' for the duration of this
    function.

    Args:
        github_user (str): The github user or org being searched.
        template (str, optional): The template git repo path. If provided, lists
            all projects that have been created with the provided template. Note
            that the template path is the SSH path
            (e.g. git@github.com:CloverHealth/temple.git)

    Returns:
        dict: A dictionary of repository information keyed on the SSH Github url

    Raises:
        `InvalidGithubUserError`: When ``github_user`` is invalid
    """
    temple.check.has_env_vars(temple.constants.GITHUB_API_TOKEN_ENV_VAR)

    if template:
        temple.check.is_git_ssh_path(template)
        search_q = 'user:{} filename:{} {}'.format(
            github_user,
            temple.constants.TEMPLE_CONFIG_FILE,
            template)
    else:
        search_q = 'user:{} cookiecutter.json in:path'.format(github_user)

    results = _code_search(search_q, github_user)
    return collections.OrderedDict(sorted(results.items()))