def start(self):
        """
        Monitors data kept in files in the predefined directory in a new thread.

        Note: Due to the underlying library, it may take a few milliseconds after this method is started for changes to
        start to being noticed.
        """
        with self._status_lock:
            if self._running:
                raise RuntimeError("Already running")
            self._running = True

        # Cannot re-use Observer after stopped
        self._observer = Observer()
        self._observer.schedule(self._event_handler, self._directory_location, recursive=True)
        self._observer.start()

        # Load all in directory afterwards to ensure no undetected changes between loading all and observing
        self._origin_mapped_data = self._load_all_in_directory()