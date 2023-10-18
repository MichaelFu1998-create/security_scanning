def run_cmd(cmd, echo=False, fail_silently=False, **kwargs):
    r"""Call given command with ``subprocess.call`` function.

    :param cmd: Command to run.
    :type cmd: tuple or str
    :param echo:
        If enabled show command to call and its output in STDOUT, otherwise
        hide all output. By default: False
    :param fail_silently: Do not raise exception on error. By default: False
    :param \*\*kwargs:
        Additional keyword arguments to be passed to ``subprocess.call``
        function. STDOUT and STDERR streams would be setup inside of function
        to ensure hiding command output in case of disabling ``echo``.
    """
    out, err = None, None

    if echo:
        cmd_str = cmd if isinstance(cmd, string_types) else ' '.join(cmd)
        kwargs['stdout'], kwargs['stderr'] = sys.stdout, sys.stderr
        print_message('$ {0}'.format(cmd_str))
    else:
        out, err = get_temp_streams()
        kwargs['stdout'], kwargs['stderr'] = out, err

    try:
        retcode = subprocess.call(cmd, **kwargs)
    except subprocess.CalledProcessError as err:
        if fail_silently:
            return False
        print_error(str(err) if IS_PY3 else unicode(err))  # noqa
    finally:
        if out:
            out.close()
        if err:
            err.close()

    if retcode and echo and not fail_silently:
        print_error('Command {0!r} returned non-zero exit status {1}'.
                    format(cmd_str, retcode))

    return retcode