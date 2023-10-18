def _augment_images_worker(self, augseq, queue_source, queue_result, seedval):
        """
        Augment endlessly images in the source queue.

        This is a worker function for that endlessly queries the source queue (input batches),
        augments batches in it and sends the result to the output queue.

        """
        np.random.seed(seedval)
        random.seed(seedval)
        augseq.reseed(seedval)
        ia.seed(seedval)

        loader_finished = False

        while not loader_finished:
            # wait for a new batch in the source queue and load it
            try:
                batch_str = queue_source.get(timeout=0.1)
                batch = pickle.loads(batch_str)
                if batch is None:
                    loader_finished = True
                    # put it back in so that other workers know that the loading queue is finished
                    queue_source.put(pickle.dumps(None, protocol=-1))
                else:
                    batch_aug = augseq.augment_batch(batch)

                    # send augmented batch to output queue
                    batch_str = pickle.dumps(batch_aug, protocol=-1)
                    queue_result.put(batch_str)
            except QueueEmpty:
                time.sleep(0.01)

        queue_result.put(pickle.dumps(None, protocol=-1))
        time.sleep(0.01)