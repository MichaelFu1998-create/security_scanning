def get_day_start_ut_span(self):
        """
        Return the first and last day_start_ut

        Returns
        -------
        first_day_start_ut: int
        last_day_start_ut: int
        """
        cur = self.conn.cursor()
        first_day_start_ut, last_day_start_ut = \
            cur.execute("SELECT min(day_start_ut), max(day_start_ut) FROM days;").fetchone()
        return first_day_start_ut, last_day_start_ut