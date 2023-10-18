def _compute_number_of_frequency_generated_stop_times(self, gtfs_source_path):
        """
        Parameters
        ----------
        Same as for "_frequency_generated_trips_rows" but for stop times table
        gtfs_source_path:
        table_name:

        Return
        ------
        """
        df_freq = self._frequency_generated_trips_rows(gtfs_source_path, return_df_freq=True)
        df_stop_times = source_csv_to_pandas(gtfs_source_path, "stop_times")
        df_stop_freq = pd.merge(df_freq, df_stop_times, how='outer', on='trip_id')
        return int(df_stop_freq['n_trips'].fillna(1).sum(axis=0))