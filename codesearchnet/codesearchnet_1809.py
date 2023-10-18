def fromtimestamp(cls, timestamp, tz=None):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """
        _check_tzinfo_arg(tz)
        converter = _time.localtime if tz is None else _time.gmtime
        self = cls._from_timestamp(converter, timestamp, tz)
        if tz is not None:
            self = tz.fromutc(self)
        return self