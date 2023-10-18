def execute(helper, config, args):
    """
    Deploys to an environment
    """
    version_label = args.version_label
    env_config = parse_env_config(config, args.environment)
    env_name = args.environment

    # upload or build an archive
    version_label = upload_application_archive(
        helper, env_config, archive=args.archive,
        directory=args.directory, version_label=version_label)

    import datetime
    start_time = datetime.datetime.utcnow().isoformat() + 'Z'
    # deploy it
    helper.deploy_version(env_name, version_label)

    # wait
    if not args.dont_wait:
        helper.wait_for_environments(env_name, status='Ready',
                                     version_label=version_label,
                                     include_deleted=False)

    # update it
    env = parse_env_config(config, env_name)
    option_settings = parse_option_settings(env.get('option_settings', {}))
    helper.update_environment(env_name,
                              description=env.get('description', None),
                              option_settings=option_settings,
                              tier_type=env.get('tier_type'),
                              tier_name=env.get('tier_name'),
                              tier_version=env.get('tier_version'))

    # wait
    if not args.dont_wait:
        helper.wait_for_environments(env_name, health='Green',
                                     status='Ready', version_label=version_label,
                                     include_deleted=False)

    events = helper.ebs.describe_events(start_time=start_time, environment_name=env_name)
    import json
    if args.log_events_to_file:
        with open('ebs_events.json', 'w+') as f:
            json.dump(events, f)

    # delete unused
    helper.delete_unused_versions(versions_to_keep=int(get(config, 'app.versions_to_keep', 10)))