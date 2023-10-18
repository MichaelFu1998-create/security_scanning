def execute(helper, config, args):
    """
    dump command dumps things
    """
    env = parse_env_config(config, args.environment)
    option_settings = env.get('option_settings', {})
    settings = parse_option_settings(option_settings)
    for setting in settings:
        out(str(setting))