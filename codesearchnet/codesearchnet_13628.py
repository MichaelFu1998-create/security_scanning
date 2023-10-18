def handle_write(self):
        """
        Handle the 'channel writable' state. E.g. send buffered data via a
        socket.
        """
        with self.lock:
            logger.debug("handle_write: queue: {0!r}".format(self._write_queue))
            try:
                job = self._write_queue.popleft()
            except IndexError:
                return
            if isinstance(job, WriteData):
                self._do_write(job.data) # pylint: disable=E1101
            elif isinstance(job, ContinueConnect):
                self._continue_connect()
            elif isinstance(job, StartTLS):
                self._initiate_starttls(**job.kwargs)
            elif isinstance(job, TLSHandshake):
                self._continue_tls_handshake()
            else:
                raise ValueError("Unrecognized job in the write queue: "
                                        "{0!r}".format(job))