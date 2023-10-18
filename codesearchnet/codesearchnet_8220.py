def start(self, threaded):
        """Creates and starts the project."""
        self.stop()
        self.__class__._INSTANCE = weakref.ref(self)
        self.is_running = True

        if threaded:
            self.thread = runnable.LoopThread()
            self.thread.run_once = self._target
            self.thread.start()
        else:
            self._target()