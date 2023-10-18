def close(self):
    """ Close the policy instance and its shared database connection. """
    self._logger.info("Closing")
    if self._conn is not None:
      self._conn.close()
      self._conn = None
    else:
      self._logger.warning(
        "close() called, but connection policy was alredy closed")
    return