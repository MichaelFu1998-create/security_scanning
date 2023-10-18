def _run_supervisor(self):
        """
        Poll the queues that the worker can use to communicate with the 
        supervisor, until all the workers are done and all the queues are 
        empty.  Handle messages as they appear.
        """
        import time

        still_supervising = lambda: (
                multiprocessing.active_children()
                or not self.log_queue.empty()
                or not self.exception_queue.empty())

        try:
            while still_supervising():
                # When a log message is received, make a logger with the same 
                # name in this process and use it to re-log the message.  It 
                # will get handled in this process.

                try:
                    record = self.log_queue.get_nowait()
                    logger = logging.getLogger(record.name)
                    logger.handle(record)
                except queue.Empty:
                    pass

                # When an exception is received, immediately re-raise it.

                try:
                    exception = self.exception_queue.get_nowait()
                except queue.Empty:
                    pass
                else:
                    raise exception

                # Sleep for a little bit, and make sure that the workers haven't 
                # outlived their time limit.

                time.sleep(1/self.frame_rate)
                self.elapsed_time += 1/self.frame_rate

                if self.time_limit and self.elapsed_time > self.time_limit:
                    raise RuntimeError("timeout")

        # Make sure the workers don't outlive the supervisor, no matter how the 
        # polling loop ended (e.g. normal execution or an exception).

        finally:
            for process in multiprocessing.active_children():
                process.terminate()