def redirect_to_env_paths(path):
    '''Get environment path from redirect file'''

    with open(path, 'r') as f:
        redirected = f.read()

    return shlex.split(redirected)