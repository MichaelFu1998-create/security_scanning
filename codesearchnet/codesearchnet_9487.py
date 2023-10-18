def parse_ls_date(self, s, *, now=None):
        """
        Parsing dates from the ls unix utility. For example,
        "Nov 18  1958" and "Nov 18 12:29".

        :param s: ls date
        :type s: :py:class:`str`

        :rtype: :py:class:`str`
        """
        with setlocale("C"):
            try:
                if now is None:
                    now = datetime.datetime.now()
                d = datetime.datetime.strptime(s, "%b %d %H:%M")
                d = d.replace(year=now.year)
                diff = (now - d).total_seconds()
                if diff > HALF_OF_YEAR_IN_SECONDS:
                    d = d.replace(year=now.year + 1)
                elif diff < -HALF_OF_YEAR_IN_SECONDS:
                    d = d.replace(year=now.year - 1)
            except ValueError:
                d = datetime.datetime.strptime(s, "%b %d  %Y")
        return self.format_date_time(d)