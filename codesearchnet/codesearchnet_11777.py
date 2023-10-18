def write_temp_file_or_dryrun(content, *args, **kwargs):
    """
    Writes the given content to a local temporary file.
    """
    dryrun = get_dryrun(kwargs.get('dryrun'))
    if dryrun:
        fd, tmp_fn = tempfile.mkstemp()
        os.remove(tmp_fn)
        cmd_run = 'local'
        cmd = 'cat <<EOT >> %s\n%s\nEOT' % (tmp_fn, content)
        if BURLAP_COMMAND_PREFIX:
            print('%s %s: %s' % (render_command_prefix(), cmd_run, cmd))
        else:
            print(cmd)
    else:
        fd, tmp_fn = tempfile.mkstemp()
        fout = open(tmp_fn, 'w')
        fout.write(content)
        fout.close()
    return tmp_fn