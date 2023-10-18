def poll(self, timeout=0.0):
    """Modified version of poll() from asyncore module"""
    if self.sock_map is None:
      Log.warning("Socket map is not registered to Gateway Looper")
    readable_lst = []
    writable_lst = []
    error_lst = []

    if self.sock_map is not None:
      for fd, obj in self.sock_map.items():
        is_r = obj.readable()
        is_w = obj.writable()
        if is_r:
          readable_lst.append(fd)
        if is_w and not obj.accepting:
          writable_lst.append(fd)
        if is_r or is_w:
          error_lst.append(fd)

    # Add wakeup fd
    readable_lst.append(self.pipe_r)

    Log.debug("Will select() with timeout: " + str(timeout) + ", with map: " + str(self.sock_map))
    try:
      readable_lst, writable_lst, error_lst = \
        select.select(readable_lst, writable_lst, error_lst, timeout)
    except select.error as err:
      Log.debug("Trivial error: " + str(err))
      if err.args[0] != errno.EINTR:
        raise
      else:
        return
    Log.debug("Selected [r]: " + str(readable_lst) +
              " [w]: " + str(writable_lst) + " [e]: " + str(error_lst))

    if self.pipe_r in readable_lst:
      Log.debug("Read from pipe")
      os.read(self.pipe_r, 1024)
      readable_lst.remove(self.pipe_r)

    if self.sock_map is not None:
      for fd in readable_lst:
        obj = self.sock_map.get(fd)
        if obj is None:
          continue
        asyncore.read(obj)

      for fd in writable_lst:
        obj = self.sock_map.get(fd)
        if obj is None:
          continue
        asyncore.write(obj)

      for fd in error_lst:
        obj = self.sock_map.get(fd)
        if obj is None:
          continue
        # pylint: disable=W0212
        asyncore._exception(obj)