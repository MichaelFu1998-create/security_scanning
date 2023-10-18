def parse(self, group_by_stmt):
        """
        Extract the data resolution of a query in seconds
        E.g. "group by time(99s)" => 99

        :param group_by_stmt: A raw InfluxDB group by statement
        """
        if not group_by_stmt:
            return Resolution.MAX_RESOLUTION

        m = self.GROUP_BY_TIME_PATTERN.match(group_by_stmt)
        if not m:
            return None

        value = int(m.group(1))
        unit = m.group(2)
        resolution = self.convert_to_seconds(value, unit)

        # We can't have a higher resolution than the max resolution
        return max(resolution, Resolution.MAX_RESOLUTION)