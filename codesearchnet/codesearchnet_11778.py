def sed_or_dryrun(*args, **kwargs):
    """
    Wrapper around Fabric's contrib.files.sed() to give it a dryrun option.

    http://docs.fabfile.org/en/0.9.1/api/contrib/files.html#fabric.contrib.files.sed
    """
    dryrun = get_dryrun(kwargs.get('dryrun'))
    if 'dryrun' in kwargs:
        del kwargs['dryrun']

    use_sudo = kwargs.get('use_sudo', False)

    if dryrun:
        context = dict(
            filename=args[0] if len(args) >= 1 else kwargs['filename'],
            before=args[1] if len(args) >= 2 else kwargs['before'],
            after=args[2] if len(args) >= 3 else kwargs['after'],
            backup=args[3] if len(args) >= 4 else kwargs.get('backup', '.bak'),
            limit=kwargs.get('limit', ''),
        )
        cmd = 'sed -i{backup} -r -e "/{limit}/ s/{before}/{after}/g {filename}"'.format(**context)
        cmd_run = 'sudo' if use_sudo else 'run'
        if BURLAP_COMMAND_PREFIX:
            print('%s %s: %s' % (render_command_prefix(), cmd_run, cmd))
        else:
            print(cmd)
    else:
        from fabric.contrib.files import sed
        sed(*args, **kwargs)