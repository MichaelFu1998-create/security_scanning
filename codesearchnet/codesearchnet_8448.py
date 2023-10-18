def env_export(prefix, exported, env):
    """
    Define the list of 'exported' variables with 'prefix' with values from 'env'
    """

    for exp in exported:
        ENV["_".join([prefix, exp])] = env[exp]