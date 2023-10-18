def get_cookiecutter_config(template, default_config=None, version=None):
    """Obtains the configuration used for cookiecutter templating

    Args:
        template: Path to the template
        default_config (dict, optional): The default configuration
        version (str, optional): The git SHA or branch to use when
            checking out template. Defaults to latest version

    Returns:
        tuple: The cookiecutter repo directory and the config dict
    """
    default_config = default_config or {}
    config_dict = cc_config.get_user_config()
    repo_dir, _ = cc_repository.determine_repo_dir(
        template=template,
        abbreviations=config_dict['abbreviations'],
        clone_to_dir=config_dict['cookiecutters_dir'],
        checkout=version,
        no_input=True)
    context_file = os.path.join(repo_dir, 'cookiecutter.json')
    context = cc_generate.generate_context(
        context_file=context_file,
        default_context={**config_dict['default_context'], **default_config})
    return repo_dir, cc_prompt.prompt_for_config(context)