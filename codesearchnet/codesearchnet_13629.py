def starttls(self, **kwargs):
        """Request a TLS handshake on the socket ans switch
        to encrypted output.
        The handshake will start after any currently buffered data is sent.

        :Parameters:
            - `kwargs`: arguments for :std:`ssl.wrap_socket`
        """
        with self.lock:
            self.event(TLSConnectingEvent())
            self._write_queue.append(StartTLS(**kwargs))
            self._write_queue_cond.notify()