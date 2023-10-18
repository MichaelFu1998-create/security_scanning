def release(self):
    """ Release the database connection and cursor

    The receiver of the Connection instance MUST call this method in order
    to reclaim resources
    """

    self._logger.debug("Releasing: %r", self)

    # Discard self from set of outstanding instances
    if self._addedToInstanceSet:
      try:
        self._clsOutstandingInstances.remove(self)
      except:
        self._logger.exception(
          "Failed to remove self from _clsOutstandingInstances: %r;", self)
        raise

    self._releaser(dbConn=self.dbConn, cursor=self.cursor)

    self.__class__._clsNumOutstanding -= 1
    assert self._clsNumOutstanding >= 0,  \
           "_clsNumOutstanding=%r" % (self._clsNumOutstanding,)

    self._releaser = None
    self.cursor = None
    self.dbConn = None
    self._creationTracebackString = None
    self._addedToInstanceSet = False
    self._logger = None
    return