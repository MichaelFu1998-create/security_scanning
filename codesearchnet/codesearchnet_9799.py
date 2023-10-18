def generate_routable_transit_events(self, start_time_ut=None, end_time_ut=None, route_type=None):
        """
        Generates events that take place during a time interval [start_time_ut, end_time_ut].
        Each event needs to be only partially overlap the given time interval.
        Does not include walking events.
        This is just a quick and dirty implementation to get a way of quickly get a
        method for generating events compatible with the routing algorithm

        Parameters
        ----------
        start_time_ut: int
        end_time_ut: int
        route_type: ?

        Yields
        ------
        event: namedtuple
            containing:
                dep_time_ut: int
                arr_time_ut: int
                from_stop_I: int
                to_stop_I: int
                trip_I : int
                route_type : int
                seq: int
        """
        from gtfspy.networks import temporal_network
        df = temporal_network(self, start_time_ut=start_time_ut, end_time_ut=end_time_ut, route_type=route_type)
        df.sort_values("dep_time_ut", ascending=False, inplace=True)

        for row in df.itertuples():
            yield row