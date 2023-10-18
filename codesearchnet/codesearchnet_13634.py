def handle_hup(self):
        """
        Handle the 'channel hungup' state. The handler should not be writable
        after this.
        """
        with self.lock:
            if self._state == 'connecting' and self._dst_addrs:
                self._hup = False
                self._set_state("connect")
                return
        self._hup = True