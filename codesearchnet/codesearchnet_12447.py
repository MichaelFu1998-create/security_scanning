def train(self, debug=True, force=False, single_thread=False, timeout=20):
        """
        Trains all the loaded intents that need to be updated
        If a cache file exists with the same hash as the intent file,
        the intent will not be trained and just loaded from file

        Args:
            debug (bool): Whether to print a message to stdout each time a new intent is trained
            force (bool): Whether to force training if already finished
            single_thread (bool): Whether to force running in a single thread
            timeout (float): Seconds before cancelling training
        Returns:
            bool: True if training succeeded without timeout
        """
        if not self.must_train and not force:
            return
        self.padaos.compile()
        self.train_thread = Thread(target=self._train, kwargs=dict(
            debug=debug,
            single_thread=single_thread,
            timeout=timeout
        ), daemon=True)
        self.train_thread.start()
        self.train_thread.join(timeout)

        self.must_train = False
        return not self.train_thread.is_alive()