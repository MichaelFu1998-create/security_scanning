def env_to_dict(env, pathsep=os.pathsep):
    '''
    Convert a dict containing environment variables into a standard dict.
    Variables containing multiple values will be split into a list based on
    the argument passed to pathsep.

    :param env: Environment dict like os.environ.data
    :param pathsep: Path separator used to split variables
    '''

    out_dict = {}

    for k, v in env.iteritems():
        if pathsep in v:
            out_dict[k] = v.split(pathsep)
        else:
            out_dict[k] = v

    return out_dict