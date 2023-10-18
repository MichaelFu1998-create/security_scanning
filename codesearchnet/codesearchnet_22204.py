def shv(command, capture=False, ignore_error=False, cwd=None):
    """Run the given command inside the virtual environment, if available:
    """
    _setVirtualEnv()
    try:
        command = "%s; %s" % (options.virtualenv.activate_cmd, command)
    except AttributeError:
        pass
    return bash(command, capture=capture, ignore_error=ignore_error, cwd=cwd)