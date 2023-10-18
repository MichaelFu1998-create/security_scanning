def expand_envvars(env):
    '''
    Expand all environment variables in an environment dict

    :param env: Environment dict
    '''

    out_env = {}

    for k, v in env.iteritems():
        out_env[k] = Template(v).safe_substitute(env)

    # Expand twice to make sure we expand everything we possibly can
    for k, v in out_env.items():
        out_env[k] = Template(v).safe_substitute(out_env)

    return out_env