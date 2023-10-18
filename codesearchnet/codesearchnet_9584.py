def open(
        self,
        tile,
        tile_directory_zoom=None,
        matching_method="gdal",
        matching_max_zoom=None,
        matching_precision=8,
        fallback_to_higher_zoom=False,
        resampling="nearest",
        **kwargs
    ):
        """
        Return InputTile object.

        Parameters
        ----------
        tile : ``Tile``
        tile_directory_zoom : None
            If set, data will be read from exactly this zoom level
        matching_method : str ('gdal' or 'min') (default: 'gdal')
            gdal: Uses GDAL's standard method. Here, the target resolution is calculated
                by averaging the extent's pixel sizes over both x and y axes. This
                approach returns a zoom level which may not have the best quality but will
                speed up reading significantly.
            min: Returns the zoom level which matches the minimum resolution of the
                extents four corner pixels. This approach returns the zoom level with the
                best possible quality but with low performance. If the tile extent is
                outside of the destination pyramid, a TopologicalError will be raised.
        matching_max_zoom : int (default: None)
            If set, it will prevent reading from zoom levels above the maximum.
        matching_precision : int
            Round resolutions to n digits before comparing.
        fallback_to_higher_zoom : bool (default: False)
            In case no data is found at zoom level, try to read data from higher zoom
            levels. Enabling this setting can lead to many IO requests in areas with no
            data.
        resampling : string
            raster file: one of "nearest", "average", "bilinear" or "lanczos"

        Returns
        -------
        input tile : ``InputTile``
            tile view of input data
        """
        # determine tile bounds in TileDirectory CRS
        td_bounds = reproject_geometry(
            tile.bbox,
            src_crs=tile.tp.crs,
            dst_crs=self.td_pyramid.crs
        ).bounds

        # find target zoom level
        if tile_directory_zoom is not None:
            zoom = tile_directory_zoom
        else:
            zoom = tile_to_zoom_level(
                tile, dst_pyramid=self.td_pyramid, matching_method=matching_method,
                precision=matching_precision
            )
            if matching_max_zoom is not None:
                zoom = min([zoom, matching_max_zoom])

        if fallback_to_higher_zoom:
            tiles_paths = []
            # check if tiles exist otherwise try higher zoom level
            while len(tiles_paths) == 0 and zoom >= 0:
                tiles_paths = _get_tiles_paths(
                    basepath=self.path,
                    ext=self._ext,
                    pyramid=self.td_pyramid,
                    bounds=td_bounds,
                    zoom=zoom
                )
                logger.debug("%s existing tiles found at zoom %s", len(tiles_paths), zoom)
                zoom -= 1
        else:
            tiles_paths = _get_tiles_paths(
                basepath=self.path,
                ext=self._ext,
                pyramid=self.td_pyramid,
                bounds=td_bounds,
                zoom=zoom
            )
            logger.debug("%s existing tiles found at zoom %s", len(tiles_paths), zoom)
        return InputTile(
            tile,
            tiles_paths=tiles_paths,
            file_type=self._file_type,
            profile=self._profile,
            td_crs=self.td_pyramid.crs,
            resampling=resampling,
            read_as_tiledir_func=self._read_as_tiledir_func,
            **kwargs
        )