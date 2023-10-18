def overhang(self, tile):
        """
        Get the left and right absolute overflow -- the amount of box
        overhanging `tile`, can be viewed as self \\ tile (set theory relative
        complement, but in a bounding sense)
        """
        ll = np.abs(amin(self.l - tile.l, aN(0, dim=self.dim)))
        rr = np.abs(amax(self.r - tile.r, aN(0, dim=self.dim)))
        return ll, rr