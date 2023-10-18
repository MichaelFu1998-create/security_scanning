def get_home_path():
    ''':returns: your home path...CPENV_HOME env var OR ~/.cpenv'''

    home = unipath(os.environ.get('CPENV_HOME', '~/.cpenv'))
    home_modules = unipath(home, 'modules')
    if not os.path.exists(home):
        os.makedirs(home)
    if not os.path.exists(home_modules):
        os.makedirs(home_modules)
    return home