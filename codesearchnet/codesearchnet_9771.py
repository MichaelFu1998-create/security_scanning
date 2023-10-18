def get_shape_distance_between_stops(self, trip_I, from_stop_seq, to_stop_seq):
        """
        Get the distance along a shape between stops

        Parameters
        ----------
        trip_I : int
            trip_ID along which we travel
        from_stop_seq : int
            the sequence number of the 'origin' stop
        to_stop_seq : int
            the sequence number of the 'destination' stop

        Returns
        -------
        distance : float, None
            If the shape calculation succeeded, return a float, otherwise return None
            (i.e. in the case where the shapes table is empty)
        """

        query_template = "SELECT shape_break FROM stop_times WHERE trip_I={trip_I} AND seq={seq} "
        stop_seqs = [from_stop_seq, to_stop_seq]
        shape_breaks = []
        for seq in stop_seqs:
            q = query_template.format(seq=seq, trip_I=trip_I)
            shape_breaks.append(self.conn.execute(q).fetchone())
        query_template = "SELECT max(d) - min(d) " \
                         "FROM shapes JOIN trips ON(trips.shape_id=shapes.shape_id) " \
                         "WHERE trip_I={trip_I} AND shapes.seq>={from_stop_seq} AND shapes.seq<={to_stop_seq};"
        distance_query = query_template.format(trip_I=trip_I, from_stop_seq=from_stop_seq, to_stop_seq=to_stop_seq)
        return self.conn.execute(distance_query).fetchone()[0]