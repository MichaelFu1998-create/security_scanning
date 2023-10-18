def _run_io_threads(self, handler):
        """Start threads for an IOHandler.
        """
        reader = ReadingThread(self.settings, handler, daemon = self.daemon,
                                                exc_queue = self.exc_queue)
        writter = WrittingThread(self.settings, handler, daemon = self.daemon,
                                                exc_queue = self.exc_queue)
        self.io_threads += [reader, writter]
        reader.start()
        writter.start()