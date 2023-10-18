def get_children(self):
        """
        Get tile children (intersecting tiles in next zoom level).

        Returns
        -------
        children : list
            a list of ``BufferedTiles``
        """
        return [BufferedTile(t, self.pixelbuffer) for t in self._tile.get_children()]