def _pipepager(text, cmd, color):
    """Page through text by feeding it to another program.  Invoking a
    pager through this might support colors.
    """
    import subprocess
    env = dict(os.environ)

    # If we're piping to less we might support colors under the
    # condition that
    cmd_detail = cmd.rsplit('/', 1)[-1].split()
    if color is None and cmd_detail[0] == 'less':
        less_flags = os.environ.get('LESS', '') + ' '.join(cmd_detail[1:])
        if not less_flags:
            env['LESS'] = '-R'
            color = True
        elif 'r' in less_flags or 'R' in less_flags:
            color = True

    if not color:
        text = strip_ansi(text)

    c = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                         env=env)
    encoding = get_best_encoding(c.stdin)
    try:
        c.stdin.write(text.encode(encoding, 'replace'))
        c.stdin.close()
    except (IOError, KeyboardInterrupt):
        pass

    # Less doesn't respect ^C, but catches it for its own UI purposes (aborting
    # search or other commands inside less).
    #
    # That means when the user hits ^C, the parent process (click) terminates,
    # but less is still alive, paging the output and messing up the terminal.
    #
    # If the user wants to make the pager exit on ^C, they should set
    # `LESS='-K'`. It's not our decision to make.
    while True:
        try:
            c.wait()
        except KeyboardInterrupt:
            pass
        else:
            break