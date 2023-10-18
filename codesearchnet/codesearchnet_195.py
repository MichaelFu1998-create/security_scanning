def terminate(self):
        """Stop all workers."""
        if not self.join_signal.is_set():
            self.join_signal.set()
        # give minimal time to put generated batches in queue and gracefully shut down
        time.sleep(0.01)

        if self.main_worker_thread.is_alive():
            self.main_worker_thread.join()

        if self.threaded:
            for worker in self.workers:
                if worker.is_alive():
                    worker.join()
        else:
            for worker in self.workers:
                if worker.is_alive():
                    worker.terminate()
                    worker.join()

            # wait until all workers are fully terminated
            while not self.all_finished():
                time.sleep(0.001)

        # empty queue until at least one element can be added and place None as signal that BL finished
        if self.queue.full():
            self.queue.get()
        self.queue.put(pickle.dumps(None, protocol=-1))
        time.sleep(0.01)

        # clean the queue, this reportedly prevents hanging threads
        while True:
            try:
                self._queue_internal.get(timeout=0.005)
            except QueueEmpty:
                break

        if not self._queue_internal._closed:
            self._queue_internal.close()
        if not self.queue._closed:
            self.queue.close()
        self._queue_internal.join_thread()
        self.queue.join_thread()
        time.sleep(0.025)