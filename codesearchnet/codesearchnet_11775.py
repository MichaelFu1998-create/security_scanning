def append_or_dryrun(*args, **kwargs):
    """
    Wrapper around Fabric's contrib.files.append() to give it a dryrun option.

    text filename

    http://docs.fabfile.org/en/0.9.1/api/contrib/files.html#fabric.contrib.files.append
    """
    from fabric.contrib.files import append

    dryrun = get_dryrun(kwargs.get('dryrun'))

    if 'dryrun' in kwargs:
        del kwargs['dryrun']

    use_sudo = kwargs.pop('use_sudo', False)

    text = args[0] if len(args) >= 1 else kwargs.pop('text')

    filename = args[1] if len(args) >= 2 else kwargs.pop('filename')

    if dryrun:
        text = text.replace('\n', '\\n')
        cmd = 'echo -e "%s" >> %s' % (text, filename)
        cmd_run = 'sudo' if use_sudo else 'run'
        if BURLAP_COMMAND_PREFIX:
            print('%s %s: %s' % (render_command_prefix(), cmd_run, cmd))
        else:
            print(cmd)
    else:
        append(filename=filename, text=text.replace(r'\n', '\n'), use_sudo=use_sudo, **kwargs)