def map_batches_async(self, batches, chunksize=None, callback=None, error_callback=None):
        """
        Augment batches asynchonously.

        Parameters
        ----------
        batches : list of imgaug.augmentables.batches.Batch
            The batches to augment.

        chunksize : None or int, optional
            Rough indicator of how many tasks should be sent to each worker. Increasing this number can improve
            performance.

        callback : None or callable, optional
            Function to call upon finish. See `multiprocessing.Pool`.

        error_callback : None or callable, optional
            Function to call upon errors. See `multiprocessing.Pool`.

        Returns
        -------
        multiprocessing.MapResult
            Asynchonous result. See `multiprocessing.Pool`.

        """
        assert isinstance(batches, list), ("Expected to get a list as 'batches', got type %s. "
                                           + "Call imap_batches() if you use generators.") % (type(batches),)
        return self.pool.map_async(_Pool_starworker, self._handle_batch_ids(batches),
                                   chunksize=chunksize, callback=callback, error_callback=error_callback)