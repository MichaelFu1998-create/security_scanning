def call_command(cmd_name, args_strings):
    """Call CLI command with arguments and returns its return value.

    Parameters
    ----------
    cmd_name: str
        Command name or full path to the binary file.

    arg_strings: list of str
        Argument strings list.

    Returns
    -------
    return_value
        Command return value.
    """
    if not op.isabs(cmd_name):
        cmd_fullpath = which(cmd_name)
    else:
        cmd_fullpath = cmd_name

    try:
        cmd_line = [cmd_fullpath] + args_strings

        log.info('Calling: {}.'.format(cmd_line))
        retval = subprocess.check_call(cmd_line)
    except CalledProcessError as ce:
        log.exception("Error calling command {} with arguments: "
                      "{} \n With return code: {}".format(cmd_name, args_strings,
                                                          ce.returncode))
        raise
    else:
        return retval