def batch_processor(
        self, zoom=None, tile=None, multi=cpu_count(), max_chunksize=1
    ):
        """
        Process a large batch of tiles and yield report messages per tile.

        Parameters
        ----------
        zoom : list or int
            either single zoom level or list of minimum and maximum zoom level;
            None processes all (default: None)
        tile : tuple
            zoom, row and column of tile to be processed (cannot be used with
            zoom)
        multi : int
            number of workers (default: number of CPU cores)
        max_chunksize : int
            maximum number of process tiles to be queued for each worker;
            (default: 1)
        """
        if zoom and tile:
            raise ValueError("use either zoom or tile")

        # run single tile
        if tile:
            yield _run_on_single_tile(self, tile)
        # run concurrently
        elif multi > 1:
            for process_info in _run_with_multiprocessing(
                self, list(_get_zoom_level(zoom, self)), multi, max_chunksize
            ):
                yield process_info
        # run sequentially
        elif multi == 1:
            for process_info in _run_without_multiprocessing(
                self, list(_get_zoom_level(zoom, self))
            ):
                yield process_info