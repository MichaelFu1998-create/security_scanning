def get_stop_count_data(self, start_ut, end_ut):
        """
        Get stop count data.

        Parameters
        ----------
        start_ut : int
            start time in unixtime
        end_ut : int
            end time in unixtime

        Returns
        -------
        stopData : pandas.DataFrame
            each row in the stopData dataFrame is a dictionary with the following elements
                stop_I, count, lat, lon, name
            with data types
                (int, int, float, float, str)
        """
        # TODO! this function could perhaps be made a single sql query now with the new tables?
        trips_df = self.get_tripIs_active_in_range(start_ut, end_ut)
        # stop_I -> count, lat, lon, name
        stop_counts = Counter()

        # loop over all trips:
        for row in trips_df.itertuples():
            # get stop_data and store it:
            stops_seq = self.get_trip_stop_time_data(row.trip_I, row.day_start_ut)
            for stop_time_row in stops_seq.itertuples(index=False):
                if (stop_time_row.dep_time_ut >= start_ut) and (stop_time_row.dep_time_ut <= end_ut):
                    stop_counts[stop_time_row.stop_I] += 1

        all_stop_data = self.stops()
        counts = [stop_counts[stop_I] for stop_I in all_stop_data["stop_I"].values]

        all_stop_data.loc[:, "count"] = pd.Series(counts, index=all_stop_data.index)
        return all_stop_data