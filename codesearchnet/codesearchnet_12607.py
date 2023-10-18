def load(self, source, pause=False):
        """
        Loads a new source (as a file) from ``source`` (a file path or URL)
        by killing the current ``omxplayer`` process and forking a new one.

        Args:
            source (string): Path to the file to play or URL
        """
        self._source = source
        self._load_source(source)
        if pause:
            time.sleep(0.5)  # Wait for the DBus interface to be initialised
            self.pause()