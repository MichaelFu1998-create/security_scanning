def bare(self):
        "Make a Features object with no metadata; points to the same features."
        if not self.meta:
            return self
        elif self.stacked:
            return Features(self.stacked_features, self.n_pts, copy=False)
        else:
            return Features(self.features, copy=False)