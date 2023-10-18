def _particle_func(self, coords, pos, wid):
        """Draws a gaussian, range is (0,1]. Coords = [3,n]"""
        dx, dy, dz = [c - p for c,p in zip(coords, pos)]
        dr2 = dx*dx + dy*dy + dz*dz
        return np.exp(-dr2/(2*wid*wid))