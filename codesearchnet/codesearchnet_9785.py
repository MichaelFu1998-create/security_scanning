def get_spreading_trips(self, start_time_ut, lat, lon,
                            max_duration_ut=4 * 3600,
                            min_transfer_time=30,
                            use_shapes=False):
        """
        Starting from a specific point and time, get complete single source
        shortest path spreading dynamics as trips, or "events".

        Parameters
        ----------
        start_time_ut: number
            Start time of the spreading.
        lat: float
            latitude of the spreading seed location
        lon: float
            longitude of the spreading seed location
        max_duration_ut: int
            maximum duration of the spreading process (in seconds)
        min_transfer_time : int
            minimum transfer time in seconds
        use_shapes : bool
            whether to include shapes

        Returns
        -------
        trips: dict
            trips['trips'] is a list whose each element (e.g. el = trips['trips'][0])
            is a dict with the following properties:
                el['lats'] : list of latitudes
                el['lons'] : list of longitudes
                el['times'] : list of passage_times
                el['route_type'] : type of vehicle as specified by GTFS, or -1 if walking
                el['name'] : name of the route
        """
        from gtfspy.spreading.spreader import Spreader
        spreader = Spreader(self, start_time_ut, lat, lon, max_duration_ut, min_transfer_time, use_shapes)
        return spreader.spread()