def get_neighbors(self, connectedness=8):
        """
        Return tile neighbors.

        Tile neighbors are unique, i.e. in some edge cases, where both the left
        and right neighbor wrapped around the antimeridian is the same. Also,
        neighbors ouside the northern and southern TilePyramid boundaries are
        excluded, because they are invalid.

        -------------
        | 8 | 1 | 5 |
        -------------
        | 4 | x | 2 |
        -------------
        | 7 | 3 | 6 |
        -------------

        Parameters
        ----------
        connectedness : int
            [4 or 8] return four direct neighbors or all eight.

        Returns
        -------
        list of BufferedTiles
        """
        return [
            BufferedTile(t, self.pixelbuffer)
            for t in self._tile.get_neighbors(connectedness=connectedness)
        ]