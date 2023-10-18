def count_tiles(self, minzoom, maxzoom, init_zoom=0):
        """
        Count number of tiles intersecting with geometry.

        Parameters
        ----------
        geometry : shapely geometry
        pyramid : TilePyramid
        minzoom : int
        maxzoom : int
        init_zoom : int

        Returns
        -------
        number of tiles
        """
        if (minzoom, maxzoom) not in self._count_tiles_cache:
            self._count_tiles_cache[(minzoom, maxzoom)] = count_tiles(
                self.config.area_at_zoom(), self.config.process_pyramid,
                minzoom, maxzoom, init_zoom=0
            )
        return self._count_tiles_cache[(minzoom, maxzoom)]