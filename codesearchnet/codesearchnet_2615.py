def poll(self):
    """Poll from the buffer

    It is a non-blocking operation, and when the buffer is empty, it raises Queue.Empty exception
    """
    try:
      # non-blocking
      ret = self._buffer.get(block=False)
      if self._producer_callback is not None:
        self._producer_callback()
      return ret
    except Queue.Empty:
      Log.debug("%s: Empty in poll()" % str(self))
      raise Queue.Empty