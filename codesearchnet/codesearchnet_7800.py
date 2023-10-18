def setup_database(config_data):
    """
    Run the migrate command to create the database schema

    :param config_data: configuration data
    """
    with chdir(config_data.project_directory):
        env = deepcopy(dict(os.environ))
        env[str('DJANGO_SETTINGS_MODULE')] = str('{0}.settings'.format(config_data.project_name))
        env[str('PYTHONPATH')] = str(os.pathsep.join(map(shlex_quote, sys.path)))
        commands = []

        commands.append(
            [sys.executable, '-W', 'ignore', 'manage.py', 'migrate'],
        )

        if config_data.verbose:
            sys.stdout.write(
                'Database setup commands: {0}\n'.format(
                    ', '.join([' '.join(cmd) for cmd in commands])
                )
            )
        for command in commands:
            try:
                output = subprocess.check_output(
                    command, env=env, stderr=subprocess.STDOUT
                )
                sys.stdout.write(output.decode('utf-8'))
            except subprocess.CalledProcessError as e:  # pragma: no cover
                if config_data.verbose:
                    sys.stdout.write(e.output.decode('utf-8'))
                raise

        if not config_data.no_user:
            sys.stdout.write('Creating admin user\n')
            if config_data.noinput:
                create_user(config_data)
            else:
                subprocess.check_call(' '.join(
                    [sys.executable, '-W', 'ignore', 'manage.py', 'createsuperuser']
                ), shell=True, stderr=subprocess.STDOUT)