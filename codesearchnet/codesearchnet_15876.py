def exit(self):
        """Quits this octave session and cleans up.
        """
        if self._engine:
            self._engine.repl.terminate()
        self._engine = None