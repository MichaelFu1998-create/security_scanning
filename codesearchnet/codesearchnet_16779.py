def execute(helper, config, args):
    """
    Swaps old and new URLs.
    If old_environment was active, new_environment will become the active environment
    """
    old_env_name = args.old_environment
    new_env_name = args.new_environment

    # swap C-Names
    out("Assuming that {} is the currently active environment...".format(old_env_name))
    out("Swapping environment cnames: {} will become active, {} will become inactive.".format(new_env_name,
                                                                                              old_env_name))
    helper.swap_environment_cnames(old_env_name, new_env_name)
    helper.wait_for_environments([old_env_name, new_env_name], status='Ready', include_deleted=False)