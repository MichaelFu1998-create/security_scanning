def render_to_file(template, fn=None, extra=None, **kwargs):
    """
    Returns a template to a local file.
    If no filename given, a temporary filename will be generated and returned.
    """
    import tempfile
    dryrun = get_dryrun(kwargs.get('dryrun'))
    append_newline = kwargs.pop('append_newline', True)
    style = kwargs.pop('style', 'cat') # |echo
    formatter = kwargs.pop('formatter', None)
    content = render_to_string(template, extra=extra)
    if append_newline and not content.endswith('\n'):
        content += '\n'

    if formatter and callable(formatter):
        content = formatter(content)

    if dryrun:
        if not fn:
            fd, fn = tempfile.mkstemp()
            fout = os.fdopen(fd, 'wt')
            fout.close()
    else:
        if fn:
            fout = open(fn, 'w')
        else:
            fd, fn = tempfile.mkstemp()
            fout = os.fdopen(fd, 'wt')
        fout.write(content)
        fout.close()
    assert fn

    if style == 'cat':
        cmd = 'cat <<EOF > %s\n%s\nEOF' % (fn, content)
    elif style == 'echo':
        cmd = 'echo -e %s > %s' % (shellquote(content), fn)
    else:
        raise NotImplementedError

    if BURLAP_COMMAND_PREFIX:
        print('%s run: %s' % (render_command_prefix(), cmd))
    else:
        print(cmd)

    return fn