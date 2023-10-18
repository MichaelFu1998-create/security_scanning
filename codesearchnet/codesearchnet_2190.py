def seed(self, seed): # pylint: disable=E0202
        """
        Sets the random seed of the environment to the given value (current time, if seed=None).
        Naturally deterministic Environments (e.g. ALE or some gym Envs) don't have to implement this method.

        Args:
            seed (int): The seed to use for initializing the pseudo-random number generator (default=epoch time in sec).
        Returns: The actual seed (int) used OR None if Environment did not override this method (no seeding supported).
        """
        if seed is None:
            self.env.seed = round(time.time())
        else:
            self.env.seed = seed
        return self.env.seed