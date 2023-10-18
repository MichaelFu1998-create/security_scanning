def _restart_stream(self):
        """Restart the stream as needed after SASL and StartTLS negotiation."""
        self._input_state = "restart"
        self._output_state = "restart"
        self.features = None
        self.transport.restart()
        if self.initiator:
            self._send_stream_start(self.stream_id)