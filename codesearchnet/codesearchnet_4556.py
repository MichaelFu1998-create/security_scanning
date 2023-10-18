def hold_worker(self, worker_id):
        """Puts a worker on hold, preventing scheduling of additional tasks to it.

        This is called "hold" mostly because this only stops scheduling of tasks,
        and does not actually kill the worker.

        Parameters
        ----------

        worker_id : str
            Worker id to be put on hold
        """
        c = self.command_client.run("HOLD_WORKER;{}".format(worker_id))
        logger.debug("Sent hold request to worker: {}".format(worker_id))
        return c