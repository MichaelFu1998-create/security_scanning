def tripI_takes_place_on_dsut(self, trip_I, day_start_ut):
        """
        Check that a trip takes place during a day

        Parameters
        ----------
        trip_I : int
            index of the trip in the gtfs data base
        day_start_ut : int
            the starting time of the day in unix time (seconds)

        Returns
        -------
        takes_place: bool
            boolean value describing whether the trip takes place during
            the given day or not
        """
        query = "SELECT * FROM days WHERE trip_I=? AND day_start_ut=?"
        params = (trip_I, day_start_ut)
        cur = self.conn.cursor()
        rows = list(cur.execute(query, params))
        if len(rows) == 0:
            return False
        else:
            assert len(rows) == 1, 'On a day, a trip_I should be present at most once'
            return True