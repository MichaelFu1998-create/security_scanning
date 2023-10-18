def _tile_coords(self, bounds):
        """ convert mercator bbox to tile index limits """
        tfm = partial(pyproj.transform,
                      pyproj.Proj(init="epsg:3857"),
                      pyproj.Proj(init="epsg:4326"))
        bounds = ops.transform(tfm, box(*bounds)).bounds

        # because tiles have a common corner, the tiles that cover a
        # given tile includes the adjacent neighbors.
        # https://github.com/mapbox/mercantile/issues/84#issuecomment-413113791

        west, south, east, north = bounds
        epsilon = 1.0e-10
        if east != west and north != south:
            # 2D bbox
            # shrink the bounds a small amount so that
            # shapes/tiles round trip.
            west += epsilon
            south += epsilon
            east -= epsilon
            north -= epsilon

        params = [west, south, east, north, [self.zoom_level]]
        tile_coords = [(tile.x, tile.y) for tile in mercantile.tiles(*params)]
        xtiles, ytiles = zip(*tile_coords)
        minx = min(xtiles)
        miny = min(ytiles)
        maxx = max(xtiles) 
        maxy = max(ytiles)
        return minx, miny, maxx, maxy