def _cookiecutter_configs_have_changed(template, old_version, new_version):
    """Given an old version and new version, check if the cookiecutter.json files have changed

    When the cookiecutter.json files change, it means the user will need to be prompted for
    new context

    Args:
        template (str): The git SSH path to the template
        old_version (str): The git SHA of the old version
        new_version (str): The git SHA of the new version

    Returns:
        bool: True if the cookiecutter.json files have been changed in the old and new versions
    """
    temple.check.is_git_ssh_path(template)
    repo_path = temple.utils.get_repo_path(template)
    github_client = temple.utils.GithubClient()
    api = '/repos/{}/contents/cookiecutter.json'.format(repo_path)

    old_config_resp = github_client.get(api, params={'ref': old_version})
    old_config_resp.raise_for_status()
    new_config_resp = github_client.get(api, params={'ref': new_version})
    new_config_resp.raise_for_status()

    return old_config_resp.json()['content'] != new_config_resp.json()['content']