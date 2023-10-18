def tiles_from_geom(self, geometry, zoom):
        """
        Return all tiles intersecting with input geometry.

        Parameters
        ----------
        geometry : ``shapely.geometry``
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : ``BufferedTile``
        """
        for tile in self.tile_pyramid.tiles_from_geom(geometry, zoom):
            yield self.tile(*tile.id)