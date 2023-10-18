def time(self, t):
        """Convert any timestamp into a datetime and save as _time"""
        _time = arrow.get(t).format('YYYY-MM-DDTHH:mm:ss')
        self._time = datetime.datetime.strptime(_time, '%Y-%m-%dT%H:%M:%S')