def _start_thread(self):
        """Start a new working thread unless the maximum number of threads
        has been reached or the request queue is empty.
        """
        with self.lock:
            if self.threads and self.queue.empty():
                return
            if len(self.threads) >= self.max_threads:
                return
            thread_n = self.last_thread_n + 1
            self.last_thread_n = thread_n
            thread = threading.Thread(target = self._run,
                            name = "{0!r} #{1}".format(self, thread_n),
                            args = (thread_n,))
            self.threads.append(thread)
            thread.daemon = True
            thread.start()