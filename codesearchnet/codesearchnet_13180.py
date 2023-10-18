def get_datetime(self, timestamp: str, unix=True):
        """Converts a %Y%m%dT%H%M%S.%fZ to a UNIX timestamp
        or a datetime.datetime object

        Parameters
        ---------
        timestamp: str
            A timstamp in the %Y%m%dT%H%M%S.%fZ format, usually returned by the API
            in the ``created_time`` field for example (eg. 20180718T145906.000Z)
        unix: Optional[bool] = True
            Whether to return a POSIX timestamp (seconds since epoch) or not

        Returns int or datetime.datetime
        """
        time = datetime.strptime(timestamp, '%Y%m%dT%H%M%S.%fZ')
        if unix:
            return int(time.timestamp())
        else:
            return time