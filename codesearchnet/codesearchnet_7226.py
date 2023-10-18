def _get_date_str(timestamp, datetimefmt, show_date=False):
        """Convert UTC datetime into user interface string."""
        fmt = ''
        if show_date:
            fmt += '\n'+datetimefmt.get('date', '')+'\n'
        fmt += datetimefmt.get('time', '')
        return timestamp.astimezone(tz=None).strftime(fmt)