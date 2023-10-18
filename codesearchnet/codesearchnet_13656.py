def start(self, daemon = False):
        """Start the threads."""
        self.daemon = daemon
        self.io_threads = []
        self.event_thread = EventDispatcherThread(self.event_dispatcher,
                                    daemon = daemon, exc_queue = self.exc_queue)
        self.event_thread.start()
        for handler in self.io_handlers:
            self._run_io_threads(handler)
        for handler in self.timeout_handlers:
            self._run_timeout_threads(handler)