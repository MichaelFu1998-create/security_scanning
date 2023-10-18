def translate(self, dr):
        """
        Translate a tile by an amount dr

        >>> Tile(5).translate(1)
        Tile [1, 1, 1] -> [6, 6, 6] ([5, 5, 5])
        """
        tile = self.copy()
        tile.l += dr
        tile.r += dr
        return tile