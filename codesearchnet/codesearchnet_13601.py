def _run(self, thread_n):
        """The thread function."""
        try:
            logger.debug("{0!r}: entering thread #{1}"
                                                .format(self, thread_n))
            resolver = self._make_resolver()
            while True:
                request = self.queue.get()
                if request is None:
                    break
                method, args = request
                logger.debug(" calling {0!r}.{1}{2!r}"
                                            .format(resolver, method, args))
                getattr(resolver, method)(*args) # pylint: disable=W0142
                self.queue.task_done()
            logger.debug("{0!r}: leaving thread #{1}"
                                                .format(self, thread_n))
        finally:
            self.threads.remove(threading.currentThread())