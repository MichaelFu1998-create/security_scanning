def get_directly_accessible_stops_within_distance(self, stop, distance):
        """
        Returns stops that are accessible without transfer from the stops that are within a specific walking distance
        :param stop: int
        :param distance: int
        :return:
        """
        query = """SELECT stop.* FROM
                    (SELECT st2.* FROM 
                    (SELECT * FROM stop_distances
                    WHERE from_stop_I = %s) sd,
                    (SELECT * FROM stop_times) st1,
                    (SELECT * FROM stop_times) st2
                    WHERE sd.d < %s AND sd.to_stop_I = st1.stop_I AND st1.trip_I = st2.trip_I 
                    GROUP BY st2.stop_I) sq,
                    (SELECT * FROM stops) stop
                    WHERE sq.stop_I = stop.stop_I""" % (stop, distance)
        return pd.read_sql_query(query, self.conn)