def is_home_environment(path):
    '''Returns True if path is in CPENV_HOME'''

    home = unipath(os.environ.get('CPENV_HOME', '~/.cpenv'))
    path = unipath(path)

    return path.startswith(home)