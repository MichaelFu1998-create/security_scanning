def create_project(config_data):
    """
    Call django-admin to create the project structure

    :param config_data: configuration data
    """
    env = deepcopy(dict(os.environ))
    env[str('DJANGO_SETTINGS_MODULE')] = str('{0}.settings'.format(config_data.project_name))
    env[str('PYTHONPATH')] = str(os.pathsep.join(map(shlex_quote, sys.path)))
    kwargs = {}
    args = []
    if config_data.template:
        kwargs['template'] = config_data.template
    args.append(config_data.project_name)
    if config_data.project_directory:
        args.append(config_data.project_directory)
        if not os.path.exists(config_data.project_directory):
            os.makedirs(config_data.project_directory)
    base_cmd = 'django-admin.py'
    start_cmds = [os.path.join(os.path.dirname(sys.executable), base_cmd)]
    start_cmd_pnodes = ['Scripts']
    start_cmds.extend([
        os.path.join(os.path.dirname(sys.executable), pnode, base_cmd)
        for pnode in start_cmd_pnodes
    ])
    start_cmd = [base_cmd]
    for p in start_cmds:
        if os.path.exists(p):
            start_cmd = [sys.executable, p]
            break
    cmd_args = start_cmd + ['startproject'] + args
    if config_data.verbose:
        sys.stdout.write('Project creation command: {0}\n'.format(' '.join(cmd_args)))
    try:
        output = subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
        sys.stdout.write(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:  # pragma: no cover
        if config_data.verbose:
            sys.stdout.write(e.output.decode('utf-8'))
        raise