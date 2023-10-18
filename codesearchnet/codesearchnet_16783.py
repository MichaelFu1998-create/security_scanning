def execute(helper, config, args):
    """
    The init command
    """

    # check to see if the application exists
    if not helper.application_exists():
        helper.create_application(get(config, 'app.description'))
    else:
        out("Application "+get(config, 'app.app_name')+" exists")

    # create environments
    environment_names = []
    environments_to_wait_for_green = []
    for env_name, env_config in list(get(config, 'app.environments').items()):
        environment_names.append(env_name)
        env_config = parse_env_config(config, env_name)
        if not helper.environment_exists(env_name):
            option_settings = parse_option_settings(env_config.get('option_settings', {}))
            helper.create_environment(env_name,
                solution_stack_name=env_config.get('solution_stack_name'),
                cname_prefix=env_config.get('cname_prefix', None),
                description=env_config.get('description', None),
                option_settings=option_settings,
                tier_name=env_config.get('tier_name'),
                tier_type=env_config.get('tier_type'),
                tier_version=env_config.get('tier_version'),
                version_label=args.version_label)
            environments_to_wait_for_green.append(env_name)
        else:
            out("Environment "+env_name)

    # get the environments
    environments_to_wait_for_term = []
    if args.delete:
        environments = helper.get_environments()
        for env in environments:
            if env['EnvironmentName'] not in environment_names:
                if env['Status'] != 'Ready':
                    out("Unable to delete "+env['EnvironmentName']+" because it's not in status Ready ("+env['Status']+")")
                else:
                    out("Deleting environment: "+env['EnvironmentName'])
                    helper.delete_environment(env['EnvironmentName'])
                    environments_to_wait_for_term.append(env['EnvironmentName'])

    # wait
    if not args.dont_wait and len(environments_to_wait_for_green)>0:
        helper.wait_for_environments(environments_to_wait_for_green, status='Ready', include_deleted=False)
    if not args.dont_wait and len(environments_to_wait_for_term)>0:
        helper.wait_for_environments(environments_to_wait_for_term, status='Terminated', include_deleted=False)

    out("Application initialized")
    return 0