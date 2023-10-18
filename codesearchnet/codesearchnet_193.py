def imap_batches_unordered(self, batches, chunksize=1):
        """
        Augment batches from a generator in a way that does not guarantee to preserve order.

        Parameters
        ----------
        batches : generator of imgaug.augmentables.batches.Batch
            The batches to augment, provided as a generator. Each call to the generator should yield exactly one
            batch.

        chunksize : None or int, optional
            Rough indicator of how many tasks should be sent to each worker. Increasing this number can improve
            performance.

        Yields
        ------
        imgaug.augmentables.batches.Batch
            Augmented batch.

        """
        assert ia.is_generator(batches), ("Expected to get a generator as 'batches', got type %s. "
                                          + "Call map_batches() if you use lists.") % (type(batches),)
        # TODO change this to 'yield from' once switched to 3.3+
        gen = self.pool.imap_unordered(_Pool_starworker, self._handle_batch_ids_gen(batches), chunksize=chunksize)
        for batch in gen:
            yield batch