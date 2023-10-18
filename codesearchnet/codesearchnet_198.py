def terminate(self):
        """
        Terminates all background processes immediately.

        This will also free their RAM.

        """
        for worker in self.workers:
            if worker.is_alive():
                worker.terminate()
        self.nb_workers_finished = len(self.workers)

        if not self.queue_result._closed:
            self.queue_result.close()
        time.sleep(0.01)