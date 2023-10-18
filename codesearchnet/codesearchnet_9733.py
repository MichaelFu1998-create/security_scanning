def _frequency_generated_trips_rows(self, gtfs_soure_path, return_df_freq=False):
        """
        This function calculates the equivalent rowcounts for trips when
        taking into account the generated rows in the gtfs object
        Parameters
        ----------
        gtfs_soure_path: path to the source file
        param txt: txt file in question
        :return: sum of all trips
        """
        df_freq = source_csv_to_pandas(gtfs_soure_path, 'frequencies')
        df_trips = source_csv_to_pandas(gtfs_soure_path, "trips")
        df_freq['n_trips'] = df_freq.apply(lambda row: len(range(str_time_to_day_seconds(row['start_time']),
                                                                 str_time_to_day_seconds(row['end_time']),
                                                                 row['headway_secs'])), axis=1)
        df_trips_freq = pd.merge(df_freq, df_trips, how='outer', on='trip_id')
        n_freq_generated_trips = int(df_trips_freq['n_trips'].fillna(1).sum(axis=0))
        if return_df_freq:
            return df_trips_freq
        else:
            return n_freq_generated_trips