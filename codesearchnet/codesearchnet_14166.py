def run(self):
        """
        The body of the tread: read lines and put them on the queue.
        """
        try:
            for line in iter(self._fd.readline, False):
                if line is not None:
                    if self._althandler:
                        if self._althandler(line):
                            # If the althandler returns True
                            # then don't process this as usual
                            continue
                self._queue.put(line)
                if not line:
                    time.sleep(0.1)
        except ValueError:  # This can happen if we are closed during readline - TODO - better fix.
            if not self._fd.closed:
                raise