def create_user(config_data):
    """
    Create admin user without user input

    :param config_data: configuration data
    """
    with chdir(os.path.abspath(config_data.project_directory)):
        env = deepcopy(dict(os.environ))
        env[str('DJANGO_SETTINGS_MODULE')] = str('{0}.settings'.format(config_data.project_name))
        env[str('PYTHONPATH')] = str(os.pathsep.join(map(shlex_quote, sys.path)))
        subprocess.check_call(
            [sys.executable, 'create_user.py'], env=env, stderr=subprocess.STDOUT
        )
        for ext in ['py', 'pyc']:
            try:
                os.remove('create_user.{0}'.format(ext))
            except OSError:
                pass