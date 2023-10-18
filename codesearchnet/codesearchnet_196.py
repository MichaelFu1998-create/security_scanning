def get_batch(self):
        """
        Returns a batch from the queue of augmented batches.

        If workers are still running and there are no batches in the queue,
        it will automatically wait for the next batch.

        Returns
        -------
        out : None or imgaug.Batch
            One batch or None if all workers have finished.

        """
        if self.all_finished():
            return None

        batch_str = self.queue_result.get()
        batch = pickle.loads(batch_str)
        if batch is not None:
            return batch
        else:
            self.nb_workers_finished += 1
            if self.nb_workers_finished >= self.nb_workers:
                try:
                    self.queue_source.get(timeout=0.001)  # remove the None from the source queue
                except QueueEmpty:
                    pass
                return None
            else:
                return self.get_batch()