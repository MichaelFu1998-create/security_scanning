def execute(helper, config, args):
    """
    Deletes an environment
    """
    helper.delete_application()

    # wait
    if not args.dont_wait:

        # get environments
        environment_names = []
        for env in helper.get_environments():
            environment_names.append(env['EnvironmentName'])

        # wait for them
        helper.wait_for_environments(environment_names, status='Terminated')
    return 0