def map_batches(self, batches, chunksize=None):
        """
        Augment batches.

        Parameters
        ----------
        batches : list of imgaug.augmentables.batches.Batch
            The batches to augment.

        chunksize : None or int, optional
            Rough indicator of how many tasks should be sent to each worker. Increasing this number can improve
            performance.

        Returns
        -------
        list of imgaug.augmentables.batches.Batch
            Augmented batches.

        """
        assert isinstance(batches, list), ("Expected to get a list as 'batches', got type %s. "
                                           + "Call imap_batches() if you use generators.") % (type(batches),)
        return self.pool.map(_Pool_starworker, self._handle_batch_ids(batches), chunksize=chunksize)