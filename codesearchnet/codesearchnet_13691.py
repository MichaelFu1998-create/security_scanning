def stream_end(self):
        """Process </stream:stream> (stream end) tag received from peer.
        """
        logger.debug("Stream ended")
        with self.lock:
            self._input_state = "closed"
            self.transport.disconnect()
            self._output_state = "closed"