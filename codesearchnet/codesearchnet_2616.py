def offer(self, item):
    """Offer to the buffer

    It is a non-blocking operation, and when the buffer is full, it raises Queue.Full exception
    """
    try:
      # non-blocking
      self._buffer.put(item, block=False)
      if self._consumer_callback is not None:
        self._consumer_callback()
      return True
    except Queue.Full:
      Log.debug("%s: Full in offer()" % str(self))
      raise Queue.Full