def _vps(self, inds):
        """Clips a list of inds to be on [0, self.N]"""
        return [j for j in inds if j >= 0 and j < self.N]