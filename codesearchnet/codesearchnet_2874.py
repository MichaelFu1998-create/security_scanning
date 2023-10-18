def read(self, dispatcher):
    """Reads incoming data from asyncore.dispatcher"""
    try:
      if not self.is_header_read:
        # try reading header
        to_read = HeronProtocol.HEADER_SIZE - len(self.header)
        self.header += dispatcher.recv(to_read)
        if len(self.header) == HeronProtocol.HEADER_SIZE:
          self.is_header_read = True
        else:
          Log.debug("Header read incomplete; read %d bytes of header" % len(self.header))
          return

      if self.is_header_read and not self.is_complete:
        # try reading data
        to_read = self.get_datasize() - len(self.data)
        self.data += dispatcher.recv(to_read)
        if len(self.data) == self.get_datasize():
          self.is_complete = True
    except socket.error as e:
      if e.errno == socket.errno.EAGAIN or e.errno == socket.errno.EWOULDBLOCK:
        # Try again later -> call continue_read later
        Log.debug("Try again error")
      else:
        # Fatal error
        Log.debug("Fatal error when reading IncomingPacket")
        raise RuntimeError("Fatal error occured in IncomingPacket.read()")