def check_call(cmd_args):
    """
    Calls the command

    Parameters
    ----------
    cmd_args: list of str
        Command name to call and its arguments in a list.

    Returns
    -------
    Command output
    """
    p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    return output