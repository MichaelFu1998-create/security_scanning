def _start_queue_management_thread(self):
        """ TODO: docstring """
        if self._queue_management_thread is None:
            logger.debug("Starting queue management thread")
            self._queue_management_thread = threading.Thread(
                target=self._queue_management_worker)
            self._queue_management_thread.daemon = True
            self._queue_management_thread.start()
            logger.debug("Started queue management thread")

        else:
            logger.debug("Management thread already exists, returning")