def renderProcessStdErr(self, stderr_line):
    """ render stderr of shelled-out process
        stderr could be error message of failure of invoking process or
        normal stderr output from successfully shelled-out process.
        In the first case, ``Popen'' should fail fast and we should be able to
        get return code immediately. We then render the failure message.
        In the second case, we simply print stderr line in stderr.
        The way to handle the first case is shaky but should be the best we can
        do since we have conflicts of design goals here.
    :param stderr_line: one line from shelled-out process
    :return:
    """
    retcode = self.process.poll()
    if retcode is not None and status_type(retcode) == Status.InvocationError:
      self._do_log(Log.error, stderr_line)
    else:
      self._do_print(sys.stderr, stderr_line)