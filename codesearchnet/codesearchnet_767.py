def close(self):
    """ Close the policy instance and its database connection pool. """
    self._logger.info("Closing")

    if self._pool is not None:
      self._pool.close()
      self._pool = None
    else:
      self._logger.warning(
        "close() called, but connection policy was alredy closed")
    return