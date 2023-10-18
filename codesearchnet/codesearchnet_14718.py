def _localize(dt):
        """
        Rely on pytz.localize to ensure new result honors DST.
        """
        try:
            tz = dt.tzinfo
            return tz.localize(dt.replace(tzinfo=None))
        except AttributeError:
            return dt