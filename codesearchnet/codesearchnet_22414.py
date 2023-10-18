def close(self):
        """
        Disconnect and close *Vim*.
        """
        self._tempfile.close()
        self._process.terminate()
        if self._process.is_alive():
            self._process.kill()