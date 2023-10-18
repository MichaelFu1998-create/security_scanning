def _encode_datetime(self, dt):
        """Encode a datetime in the format '%Y-%m-%dT%H:%M:%SZ'.

        The datetime can be naieve (doesn't have timezone info) or aware
        (it does have a tzinfo attribute set). Regardless, the datetime
        is transformed into UTC.
        """
        if dt.tzinfo is None:
            # Force it to be a UTC datetime
            dt = dt.replace(tzinfo=datetime.timezone.utc)

        # Convert to UTC (no matter what)
        dt = dt.astimezone(datetime.timezone.utc)

        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')