def _trackInstanceAndCheckForConcurrencyViolation(self):
    """ Check for concurrency violation and add self to
    _clsOutstandingInstances.

    ASSUMPTION: Called from constructor BEFORE _clsNumOutstanding is
    incremented
    """
    global g_max_concurrency, g_max_concurrency_raise_exception

    assert g_max_concurrency is not None
    assert self not in self._clsOutstandingInstances, repr(self)

    # Populate diagnostic info
    self._creationTracebackString = traceback.format_stack()

    # Check for concurrency violation
    if self._clsNumOutstanding >= g_max_concurrency:
      # NOTE: It's possible for _clsNumOutstanding to be greater than
      #  len(_clsOutstandingInstances) if concurrency check was enabled after
      #  unrelease allocations.
      errorMsg = ("With numOutstanding=%r, exceeded concurrency limit=%r "
                  "when requesting %r. OTHER TRACKED UNRELEASED "
                  "INSTANCES (%s): %r") % (
        self._clsNumOutstanding, g_max_concurrency, self,
        len(self._clsOutstandingInstances), self._clsOutstandingInstances,)

      self._logger.error(errorMsg)

      if g_max_concurrency_raise_exception:
        raise ConcurrencyExceededError(errorMsg)


    # Add self to tracked instance set
    self._clsOutstandingInstances.add(self)
    self._addedToInstanceSet = True

    return