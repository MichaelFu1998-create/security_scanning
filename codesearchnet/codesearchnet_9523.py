def batch_process(
        self, zoom=None, tile=None, multi=cpu_count(), max_chunksize=1
    ):
        """
        Process a large batch of tiles.

        Parameters
        ----------
        process : MapcheteProcess
            process to be run
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
        list(self.batch_processor(zoom, tile, multi, max_chunksize))