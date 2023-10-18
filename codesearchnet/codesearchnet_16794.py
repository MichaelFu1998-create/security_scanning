def execute(helper, config, args):
    """
    Updates environments
    """
    environments = []
    if args.environment:
        for env_name in args.environment:
            environments.append(env_name)
    else:
        for env_name, env_config in list(get(config, 'app.environments').items()):
            environments.append(env_name)

    wait_environments = []
    for env_name in environments:
        env = parse_env_config(config, env_name)
        option_settings = parse_option_settings(env.get('option_settings', {}))
        helper.update_environment(env_name,
            description=env.get('description', None),
            option_settings=option_settings,
            tier_type=env.get('tier_type'),
            tier_name=env.get('tier_name'),
            tier_version=env.get('tier_version'))
        wait_environments.append(env_name)

    # wait
    if not args.dont_wait:
        helper.wait_for_environments(wait_environments, health='Green', status='Ready')