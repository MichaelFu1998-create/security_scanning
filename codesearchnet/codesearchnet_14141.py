def sbot_executable():
    """
    Find shoebot executable
    """
    gsettings=load_gsettings()
    venv = gsettings.get_string('current-virtualenv')
    if venv == 'Default':
        sbot = which('sbot')
    elif venv == 'System':
        # find system python
        env_venv = os.environ.get('VIRTUAL_ENV')
        if not env_venv:
            return which('sbot')

        # First sbot in path that is not in current venv
        for p in os.environ['PATH'].split(os.path.pathsep):
            sbot='%s/sbot' % p
            if not p.startswith(env_venv) and os.path.isfile(sbot):
                return sbot
    else:
        sbot = os.path.join(venv, 'bin/sbot')
        if not os.path.isfile(sbot):
            print('Shoebot not found, reverting to System shoebot')
            sbot = which('sbot')
    return os.path.realpath(sbot)