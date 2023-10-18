def make_views(cls, conn):
        """Create day_trips and day_stop_times views.

        day_trips:  day_trips2 x trips  = days x trips
        day_stop_times: day_trips2 x trips x stop_times = days x trips x stop_times
        """
        conn.execute('DROP VIEW IF EXISTS main.day_trips')
        conn.execute('CREATE VIEW day_trips AS   '
                     'SELECT day_trips2.*, trips.* '
                     #'days.day_start_ut+trips.start_time_ds AS start_time_ut, '
                     #'days.day_start_ut+trips.end_time_ds AS end_time_ut   '
                     'FROM day_trips2 JOIN trips USING (trip_I);')
        conn.commit()

        conn.execute('DROP VIEW IF EXISTS main.day_stop_times')
        conn.execute('CREATE VIEW day_stop_times AS   '
                     'SELECT day_trips2.*, trips.*, stop_times.*, '
                     #'days.day_start_ut+trips.start_time_ds AS start_time_ut, '
                     #'days.day_start_ut+trips.end_time_ds AS end_time_ut, '
                     'day_trips2.day_start_ut+stop_times.arr_time_ds AS arr_time_ut, '
                     'day_trips2.day_start_ut+stop_times.dep_time_ds AS dep_time_ut   '
                     'FROM day_trips2 '
                     'JOIN trips USING (trip_I) '
                     'JOIN stop_times USING (trip_I)')
        conn.commit()