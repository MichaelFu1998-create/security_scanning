def _parse_datetime(self, value):
        """ Parses a datetime string from "YYYY/MM/DD HH:MM:SS +HHMM" format

        Args:
            value (str): String

        Returns:
            datetime. Datetime
        """
        offset = 0
        pattern = r"\s+([+-]{1}\d+)\Z"
        matches = re.search(pattern, value)
        if matches:
            value = re.sub(pattern, '', value)
            offset = datetime.timedelta(hours=int(matches.group(1))/100)
        return datetime.datetime.strptime(value, "%Y/%m/%d %H:%M:%S") - offset