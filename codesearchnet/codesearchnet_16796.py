def execute(helper, config, args):
    """
    Rebuilds an environment
    """
    env_config = parse_env_config(config, args.environment)
    helper.rebuild_environment(args.environment)

    # wait
    if not args.dont_wait:
        helper.wait_for_environments(args.environment, health='Green', status='Ready')