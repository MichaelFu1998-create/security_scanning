def get_process_tiles(self, zoom=None):
        """
        Yield process tiles.

        Tiles intersecting with the input data bounding boxes as well as
        process bounds, if provided, are considered process tiles. This is to
        avoid iterating through empty tiles.

        Parameters
        ----------
        zoom : integer
            zoom level process tiles should be returned from; if none is given,
            return all process tiles

        yields
        ------
        BufferedTile objects
        """
        if zoom or zoom == 0:
            for tile in self.config.process_pyramid.tiles_from_geom(
                self.config.area_at_zoom(zoom), zoom
            ):
                yield tile
        else:
            for zoom in reversed(self.config.zoom_levels):
                for tile in self.config.process_pyramid.tiles_from_geom(
                    self.config.area_at_zoom(zoom), zoom
                ):
                    yield tile