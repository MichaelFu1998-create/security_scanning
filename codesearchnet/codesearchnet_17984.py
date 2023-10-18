def pad(self, pad):
        """
        Pad this tile by an equal amount on each side as specified by pad

        >>> Tile(10).pad(2)
        Tile [-2, -2, -2] -> [12, 12, 12] ([14, 14, 14])

        >>> Tile(10).pad([1,2,3])
        Tile [-1, -2, -3] -> [11, 12, 13] ([12, 14, 16])
        """
        tile = self.copy()
        tile.l -= pad
        tile.r += pad
        return tile