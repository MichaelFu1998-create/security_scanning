def _send_stream_error(self, condition):
        """Same as `send_stream_error`, but expects `lock` acquired.
        """
        if self._output_state is "closed":
            return
        if self._output_state in (None, "restart"):
            self._send_stream_start()
        element = StreamErrorElement(condition).as_xml()
        self.transport.send_element(element)
        self.transport.disconnect()
        self._output_state = "closed"