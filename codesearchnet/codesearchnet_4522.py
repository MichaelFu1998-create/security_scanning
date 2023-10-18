def shutdown(self):
        """Shutdown method, to kill the threads and workers."""
        self.is_alive = False
        logging.debug("Waking management thread")
        self.incoming_q.put(None)  # Wake up the thread
        self._queue_management_thread.join()  # Force join
        logging.debug("Exiting thread")
        self.worker.join()
        return True