def _ensure_started(self):
        """Ensure player backing process is started
        """
        if self._process and self._process.poll() is None:
            return

        if not getattr(self, "_cmd"):
            raise RuntimeError("Player command is not configured")

        log.debug("Starting playback command: %r", self._cmd)
        self._process = SilentPopen(self._cmd)
        self._post_start()