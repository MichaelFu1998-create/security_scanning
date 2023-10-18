def _random_point(self):
        """Find an approximately random point in the flux cone."""

        idx = np.random.randint(self.n_warmup,
                                size=min(2, np.ceil(np.sqrt(self.n_warmup))))
        return self.warmup[idx, :].mean(axis=0)