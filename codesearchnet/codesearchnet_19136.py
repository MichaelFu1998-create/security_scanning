def make_stacked(self):
        "If unstacked, convert to stacked. If stacked, do nothing."
        if self.stacked:
            return

        self._boundaries = bounds = np.r_[0, np.cumsum(self.n_pts)]
        self.stacked_features = stacked = np.vstack(self.features)
        self.features = np.array(
            [stacked[bounds[i-1]:bounds[i]] for i in xrange(1, len(bounds))],
            dtype=object)
        self.stacked = True