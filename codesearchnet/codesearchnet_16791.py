def execute(helper, config, args):
    """
    Waits for an environment to be healthy
    """
    helper.wait_for_environments(args.environment, health=args.health)