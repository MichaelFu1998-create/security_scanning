def stop(self, join = False, timeout = None):
        """Stop the threads.

        :Parameters:
            - `join`: join the threads (wait until they exit)
            - `timeout`: maximum time (in seconds) to wait when `join` is
              `True`).  No limit when `timeout` is `None`.
        """
        logger.debug("Closing the io handlers...")
        for handler in self.io_handlers:
            handler.close()
        if self.event_thread and self.event_thread.is_alive():
            logger.debug("Sending the QUIT signal")
            self.event_queue.put(QUIT)
        logger.debug("  sent")
        threads = self.io_threads + self.timeout_threads
        for thread in threads:
            logger.debug("Stopping thread: {0!r}".format(thread))
            thread.stop()
        if not join:
            return
        if self.event_thread:
            threads.append(self.event_thread)
        if timeout is None:
            for thread in threads:
                thread.join()
        else:
            timeout1 = (timeout * 0.01) / len(threads)
            threads_left = []
            for thread in threads:
                logger.debug("Quick-joining thread {0!r}...".format(thread))
                thread.join(timeout1)
                if thread.is_alive():
                    logger.debug("  thread still alive".format(thread))
                    threads_left.append(thread)
            if threads_left:
                timeout2 = (timeout * 0.99) / len(threads_left)
                for thread in threads_left:
                    logger.debug("Joining thread {0!r}...".format(thread))
                    thread.join(timeout2)
        self.io_threads = []
        self.event_thread = None