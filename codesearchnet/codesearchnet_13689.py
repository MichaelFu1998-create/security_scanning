def transport_connected(self):
        """Called when transport has been connected.

        Send the stream head if initiator.
        """
        with self.lock:
            if self.initiator:
                if self._output_state is None:
                    self._initiate()