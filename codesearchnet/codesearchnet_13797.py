def trusted_cmd(f):
    """
    Trusted commands cannot be run remotely

    :param f:
    :return:
    """
    def run_cmd(self, line):
        if self.trusted:
            f(self, line)
        else:
            print("Sorry cannot do %s here." % f.__name__[3:])

    global trusted_cmds
    trusted_cmds.add(f.__name__)
    run_cmd.__doc__ = f.__doc__
    return run_cmd