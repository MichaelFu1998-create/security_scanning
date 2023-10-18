def _tile(self, n):
        """Get the update tile surrounding particle `n` """
        pos = self._trans(self.pos[n])
        return Tile(pos, pos).pad(self.support_pad)