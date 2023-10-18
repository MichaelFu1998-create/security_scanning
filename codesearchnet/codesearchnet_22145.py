def format_time(seconds):
        """Formats time as the string "HH:MM:SS"."""

        timedelta = datetime.timedelta(seconds=int(seconds))

        mm, ss = divmod(timedelta.seconds, 60)
        if mm < 60:
            return "%02d:%02d" % (mm, ss)
        hh, mm = divmod(mm, 60)
        if hh < 24:
            return "%02d:%02d:%02d" % (hh, mm, ss)
        dd, hh = divmod(mm, 24)
        return "%d days %02d:%02d:%02d" % (dd, hh, mm, ss)