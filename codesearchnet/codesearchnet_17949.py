def _tile(self, n):
        """ Get the tile surrounding particle `n` """
        zsc = np.array([1.0/self.zscale, 1, 1])
        pos, rad = self.pos[n], self.rad[n]
        pos = self._trans(pos)
        return Tile(pos - zsc*rad, pos + zsc*rad).pad(self.support_pad)