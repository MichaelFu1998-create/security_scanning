def _env_vars_from_file(filename):
    """
    This code is copied from Docker Compose, so that we're exactly compatible
    with their `env_file` option
    """
    def split_env(env):
        if '=' in env:
            return env.split('=', 1)
        else:
            return env, None
    env = {}
    for line in open(filename, 'r'):
        line = line.strip()
        if line and not line.startswith('#'):
            k, v = split_env(line)
            env[k] = v
    return env