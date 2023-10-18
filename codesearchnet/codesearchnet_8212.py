def step(self, amt=1):
        """
        This may seem silly, but on a Receiver step() need not do anything.
        Instead, receive the data on the receive thread and set it on the buffer
        then call self._hold_for_data.set()
        """
        if not self._stop_event.isSet():
            self._hold_for_data.wait()
            self._hold_for_data.clear()