def _start_connect(self):
        """Start connecting to the next address on the `_dst_addrs` list.

        [ called with `lock` acquired ]

        """
        family, addr = self._dst_addrs.pop(0)
        self._socket = socket.socket(family, socket.SOCK_STREAM)
        self._socket.setblocking(False)
        self._dst_addr = addr
        self._family  = family
        try:
            self._socket.connect(addr)
        except socket.error, err:
            logger.debug("Connect error: {0}".format(err))
            if err.args[0] in BLOCKING_ERRORS:
                self._set_state("connecting")
                self._write_queue.append(ContinueConnect())
                self._write_queue_cond.notify()
                self.event(ConnectingEvent(addr))
                return
            elif self._dst_addrs:
                self._set_state("connect")
                return
            elif self._dst_nameports:
                self._set_state("resolve-hostname")
                return
            else:
                self._socket.close()
                self._socket = None
                self._set_state("aborted")
                self._write_queue.clear()
                self._write_queue_cond.notify()
                raise
        self._connected()