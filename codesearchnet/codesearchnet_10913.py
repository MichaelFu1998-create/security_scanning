def positions(self):
        """Initial position for each particle. Shape (N, 3, 1)."""
        return np.vstack([p.r0 for p in self]).reshape(len(self), 3, 1)