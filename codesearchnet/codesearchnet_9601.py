def tiles_from_bbox(self, geometry, zoom):
        """
        All metatiles intersecting with given bounding box.

        Parameters
        ----------
        geometry : ``shapely.geometry``
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : generator
            generates ``BufferedTiles``
        """
        for tile in self.tile_pyramid.tiles_from_bbox(geometry, zoom):
            yield self.tile(*tile.id)