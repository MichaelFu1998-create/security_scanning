def get_timezone_name(self):
        """
        Get name of the GTFS timezone

        Returns
        -------
        timezone_name : str
            name of the time zone, e.g. "Europe/Helsinki"
        """
        tz_name = self.conn.execute('SELECT timezone FROM agencies LIMIT 1').fetchone()
        if tz_name is None:
            raise ValueError("This database does not have a timezone defined.")
        return tz_name[0]