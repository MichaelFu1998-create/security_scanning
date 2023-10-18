def _cmd_exists(cmd):
    """ check if dependency program is there """
    return _subprocess.call("type " + cmd,
                           shell=True,
                           stdout=_subprocess.PIPE,
                           stderr=_subprocess.PIPE) == 0