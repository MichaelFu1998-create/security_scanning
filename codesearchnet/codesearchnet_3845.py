def stop(self):
        """
        Doctest:
            >>> CaptureStdout(enabled=False).stop()
            >>> CaptureStdout(enabled=True).stop()
        """
        if self.enabled:
            self.started = False
            sys.stdout = self.orig_stdout