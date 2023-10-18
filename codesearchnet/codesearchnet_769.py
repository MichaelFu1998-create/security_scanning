def close(self):
    """ Close the policy instance. """
    self._logger.info("Closing")

    if self._opened:
      self._opened = False
    else:
      self._logger.warning(
        "close() called, but connection policy was alredy closed")

    return