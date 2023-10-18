def _remove_closest_particle(self, p):
        """removes the closest particle in self.pos to ``p``"""
        #1. find closest pos:
        dp = self.pos - p
        dist2 = (dp*dp).sum(axis=1)
        ind = dist2.argmin()
        rp = self.pos[ind].copy()
        #2. delete
        self.pos = np.delete(self.pos, ind, axis=0)
        return rp