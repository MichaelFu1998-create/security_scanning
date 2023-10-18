def get_closest_stop(self, lat, lon):
        """
        Get closest stop to a given location.

        Parameters
        ----------
        lat: float
            latitude coordinate of the location
        lon: float
            longitude coordinate of the location

        Returns
        -------
        stop_I: int
            the index of the stop in the database
        """
        cur = self.conn.cursor()
        min_dist = float("inf")
        min_stop_I = None
        rows = cur.execute("SELECT stop_I, lat, lon FROM stops")
        for stop_I, lat_s, lon_s in rows:
            dist_now = wgs84_distance(lat, lon, lat_s, lon_s)
            if dist_now < min_dist:
                min_dist = dist_now
                min_stop_I = stop_I
        return min_stop_I