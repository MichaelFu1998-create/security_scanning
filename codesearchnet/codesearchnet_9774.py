def get_timezone_string(self, dt=None):
        """
        Return the timezone of the GTFS database object as a string.
        The assumed time when the timezone (difference) is computed
        is the download date of the file.
        This might not be optimal in all cases.

        So this function should return values like:
            "+0200" or "-1100"

        Parameters
        ----------
        dt : datetime.datetime, optional
            The (unlocalized) date when the timezone should be computed.
            Defaults first to download_date, and then to the runtime date.

        Returns
        -------
        timezone_string : str
        """
        if dt is None:
            download_date = self.meta.get('download_date')
            if download_date:
                dt = datetime.datetime.strptime(download_date, '%Y-%m-%d')
            else:
                dt = datetime.datetime.today()
        loc_dt = self._timezone.localize(dt)
        # get the timezone
        timezone_string = loc_dt.strftime("%z")
        return timezone_string