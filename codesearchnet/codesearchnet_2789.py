def renderProcessStdOut(self, stdout):
    """ render stdout of shelled-out process
        stdout always contains information Java process wants to
        propagate back to cli, so we do special rendering here
    :param stdout: all lines from shelled-out process
    :return:
    """
    # since we render stdout line based on Java process return code,
    # ``status'' has to be already set
    assert self.status is not None
    # remove pending newline
    if self.status == Status.Ok:
      self._do_log(Log.info, stdout)
    elif self.status == Status.HeronError:
      # remove last newline since logging will append newline
      self._do_log(Log.error, stdout)
    # No need to prefix [INFO] here. We want to display dry-run response in a clean way
    elif self.status == Status.DryRun:
      self._do_print(sys.stdout, stdout)
    elif self.status == Status.InvocationError:
      self._do_print(sys.stdout, stdout)
    else:
      raise RuntimeError(
          "Unknown status type of value %d. Expected value: %s" % \
          (self.status.value, list(Status)))