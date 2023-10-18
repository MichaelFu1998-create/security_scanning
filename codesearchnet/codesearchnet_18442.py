def _parse(self, timestr, dayfirst=None, yearfirst=None, fuzzy=False,
               fuzzy_with_tokens=False):
        """
        Private method which performs the heavy lifting of parsing, called from
        ``parse()``, which passes on its ``kwargs`` to this function.

        :param timestr:
            The string to parse.

        :param dayfirst:
            Whether to interpret the first value in an ambiguous 3-integer date
            (e.g. 01/05/09) as the day (``True``) or month (``False``). If
            ``yearfirst`` is set to ``True``, this distinguishes between YDM
            and YMD. If set to ``None``, this value is retrieved from the
            current :class:`parserinfo` object (which itself defaults to
            ``False``).

        :param yearfirst:
            Whether to interpret the first value in an ambiguous 3-integer date
            (e.g. 01/05/09) as the year. If ``True``, the first number is taken
            to be the year, otherwise the last number is taken to be the year.
            If this is set to ``None``, the value is retrieved from the current
            :class:`parserinfo` object (which itself defaults to ``False``).

        :param fuzzy:
            Whether to allow fuzzy parsing, allowing for string like "Today is
            January 1, 2047 at 8:21:00AM".

        :param fuzzy_with_tokens:
            If ``True``, ``fuzzy`` is automatically set to True, and the parser
            will return a tuple where the first element is the parsed
            :class:`datetime.datetime` datetimestamp and the second element is
            a tuple containing the portions of the string which were ignored:

            .. doctest::

                >>> from dateutil.parser import parse
                >>> parse("Today is January 1, 2047 at 8:21:00AM", fuzzy_with_tokens=True)
                (datetime.datetime(2047, 1, 1, 8, 21), (u'Today is ', u' ', u'at '))

        """
        if fuzzy_with_tokens:
            fuzzy = True

        info = self.info

        if dayfirst is None:
            dayfirst = info.dayfirst

        if yearfirst is None:
            yearfirst = info.yearfirst

        res = self._result()
        l = _timelex.split(timestr)         # Splits the timestr into tokens

        # keep up with the last token skipped so we can recombine
        # consecutively skipped tokens (-2 for when i begins at 0).
        last_skipped_token_i = -2
        skipped_tokens = list()

        try:
            # year/month/day list
            ymd = _ymd(timestr)

            # Index of the month string in ymd
            mstridx = -1

            len_l = len(l)
            i = 0
            while i < len_l:

                # Check if it's a number
                try:
                    value_repr = l[i]
                    value = float(value_repr)
                except ValueError:
                    value = None

                if value is not None:
                    # Token is a number
                    len_li = len(l[i])
                    i += 1

                    if (len(ymd) == 3 and len_li in (2, 4)
                        and res.hour is None and (i >= len_l or (l[i] != ':' and
                                                                 info.hms(l[i]) is None))):
                        # 19990101T23[59]
                        s = l[i - 1]
                        res.hour = int(s[:2])

                        if len_li == 4:
                            res.minute = int(s[2:])

                    elif len_li == 6 or (len_li > 6 and l[i - 1].find('.') == 6):
                        # YYMMDD or HHMMSS[.ss]
                        s = l[i - 1]

                        if not ymd and l[i - 1].find('.') == -1:
                            # ymd.append(info.convertyear(int(s[:2])))

                            ymd.append(s[:2])
                            ymd.append(s[2:4])
                            ymd.append(s[4:])
                        else:
                            # 19990101T235959[.59]
                            res.hour = int(s[:2])
                            res.minute = int(s[2:4])
                            res.second, res.microsecond = _parsems(s[4:])

                    elif len_li in (8, 12, 14):
                        # YYYYMMDD
                        s = l[i - 1]
                        ymd.append(s[:4])
                        ymd.append(s[4:6])
                        ymd.append(s[6:8])

                        if len_li > 8:
                            res.hour = int(s[8:10])
                            res.minute = int(s[10:12])

                            if len_li > 12:
                                res.second = int(s[12:])

                    elif ((i < len_l and info.hms(l[i]) is not None) or
                          (i + 1 < len_l and l[i] == ' ' and
                           info.hms(l[i + 1]) is not None)):

                        # HH[ ]h or MM[ ]m or SS[.ss][ ]s
                        if l[i] == ' ':
                            i += 1

                        idx = info.hms(l[i])

                        while True:
                            if idx == 0:
                                res.hour = int(value)

                                if value % 1:
                                    res.minute = int(60 * (value % 1))

                            elif idx == 1:
                                res.minute = int(value)

                                if value % 1:
                                    res.second = int(60 * (value % 1))

                            elif idx == 2:
                                res.second, res.microsecond = \
                                    _parsems(value_repr)

                            i += 1

                            if i >= len_l or idx == 2:
                                break

                            # 12h00
                            try:
                                value_repr = l[i]
                                value = float(value_repr)
                            except ValueError:
                                break
                            else:
                                i += 1
                                idx += 1

                                if i < len_l:
                                    newidx = info.hms(l[i])

                                    if newidx is not None:
                                        idx = newidx

                    elif (i == len_l and l[i - 2] == ' ' and
                          info.hms(l[i - 3]) is not None):
                        # X h MM or X m SS
                        idx = info.hms(l[i - 3])

                        if idx == 0:               # h
                            res.minute = int(value)

                            sec_remainder = value % 1
                            if sec_remainder:
                                res.second = int(60 * sec_remainder)
                        elif idx == 1:             # m
                            res.second, res.microsecond = \
                                _parsems(value_repr)

                        # We don't need to advance the tokens here because the
                        # i == len_l call indicates that we're looking at all
                        # the tokens already.

                    elif i + 1 < len_l and l[i] == ':':
                        # HH:MM[:SS[.ss]]
                        res.hour = int(value)
                        i += 1
                        value = float(l[i])
                        res.minute = int(value)

                        if value % 1:
                            res.second = int(60 * (value % 1))

                        i += 1

                        if i < len_l and l[i] == ':':
                            res.second, res.microsecond = _parsems(l[i + 1])
                            i += 2

                    elif i < len_l and l[i] in ('-', '/', '.'):
                        sep = l[i]
                        ymd.append(value_repr)
                        i += 1

                        if i < len_l and not info.jump(l[i]):
                            try:
                                # 01-01[-01]
                                ymd.append(l[i])
                            except ValueError:
                                # 01-Jan[-01]
                                value = info.month(l[i])

                                if value is not None:
                                    ymd.append(value)
                                    assert mstridx == -1
                                    mstridx = len(ymd) - 1
                                else:
                                    return None, None

                            i += 1

                            if i < len_l and l[i] == sep:
                                # We have three members
                                i += 1
                                value = info.month(l[i])

                                if value is not None:
                                    ymd.append(value)
                                    mstridx = len(ymd) - 1
                                    assert mstridx == -1
                                else:
                                    ymd.append(l[i])

                                i += 1
                    elif i >= len_l or info.jump(l[i]):
                        if i + 1 < len_l and info.ampm(l[i + 1]) is not None:
                            # 12 am
                            res.hour = int(value)

                            if res.hour < 12 and info.ampm(l[i + 1]) == 1:
                                res.hour += 12
                            elif res.hour == 12 and info.ampm(l[i + 1]) == 0:
                                res.hour = 0

                            i += 1
                        else:
                            # Year, month or day
                            ymd.append(value)
                        i += 1
                    elif info.ampm(l[i]) is not None:

                        # 12am
                        res.hour = int(value)

                        if res.hour < 12 and info.ampm(l[i]) == 1:
                            res.hour += 12
                        elif res.hour == 12 and info.ampm(l[i]) == 0:
                            res.hour = 0
                        i += 1

                    elif not fuzzy:
                        return None, None
                    else:
                        i += 1
                    continue

                # Check weekday
                value = info.weekday(l[i])
                if value is not None:
                    res.weekday = value
                    i += 1
                    continue

                # Check month name
                value = info.month(l[i])
                if value is not None:
                    ymd.append(value)
                    assert mstridx == -1
                    mstridx = len(ymd) - 1

                    i += 1
                    if i < len_l:
                        if l[i] in ('-', '/'):
                            # Jan-01[-99]
                            sep = l[i]
                            i += 1
                            ymd.append(l[i])
                            i += 1

                            if i < len_l and l[i] == sep:
                                # Jan-01-99
                                i += 1
                                ymd.append(l[i])
                                i += 1

                        elif (i + 3 < len_l and l[i] == l[i + 2] == ' '
                              and info.pertain(l[i + 1])):
                            # Jan of 01
                            # In this case, 01 is clearly year
                            try:
                                value = int(l[i + 3])
                            except ValueError:
                                # Wrong guess
                                pass
                            else:
                                # Convert it here to become unambiguous
                                ymd.append(str(info.convertyear(value)))
                            i += 4
                    continue

                # Check am/pm
                value = info.ampm(l[i])
                if value is not None:
                    # For fuzzy parsing, 'a' or 'am' (both valid English words)
                    # may erroneously trigger the AM/PM flag. Deal with that
                    # here.
                    val_is_ampm = True

                    # If there's already an AM/PM flag, this one isn't one.
                    if fuzzy and res.ampm is not None:
                        val_is_ampm = False

                    # If AM/PM is found and hour is not, raise a ValueError
                    if res.hour is None:
                        if fuzzy:
                            val_is_ampm = False
                        else:
                            raise ValueError('No hour specified with ' +
                                             'AM or PM flag.')
                    elif not 0 <= res.hour <= 12:
                        # If AM/PM is found, it's a 12 hour clock, so raise
                        # an error for invalid range
                        if fuzzy:
                            val_is_ampm = False
                        else:
                            raise ValueError('Invalid hour specified for ' +
                                             '12-hour clock.')

                    if val_is_ampm:
                        if value == 1 and res.hour < 12:
                            res.hour += 12
                        elif value == 0 and res.hour == 12:
                            res.hour = 0

                        res.ampm = value

                    elif fuzzy:
                        last_skipped_token_i = self._skip_token(skipped_tokens,
                                                                last_skipped_token_i, i, l)
                    i += 1
                    continue

                # Check for a timezone name
                if (res.hour is not None and len(l[i]) <= 5 and
                        res.tzname is None and res.tzoffset is None and
                        not [x for x in l[i] if x not in
                             string.ascii_uppercase]):
                    res.tzname = l[i]
                    res.tzoffset = info.tzoffset(res.tzname)
                    i += 1

                    # Check for something like GMT+3, or BRST+3. Notice
                    # that it doesn't mean "I am 3 hours after GMT", but
                    # "my time +3 is GMT". If found, we reverse the
                    # logic so that timezone parsing code will get it
                    # right.
                    if i < len_l and l[i] in ('+', '-'):
                        l[i] = ('+', '-')[l[i] == '+']
                        res.tzoffset = None
                        if info.utczone(res.tzname):
                            # With something like GMT+3, the timezone
                            # is *not* GMT.
                            res.tzname = None

                    continue

                # Check for a numbered timezone
                if res.hour is not None and l[i] in ('+', '-'):
                    signal = (-1, 1)[l[i] == '+']
                    i += 1
                    len_li = len(l[i])

                    if len_li == 4:
                        # -0300
                        res.tzoffset = int(l[i][:2]) * \
                            3600 + int(l[i][2:]) * 60
                    elif i + 1 < len_l and l[i + 1] == ':':
                        # -03:00
                        res.tzoffset = int(l[i]) * 3600 + int(l[i + 2]) * 60
                        i += 2
                    elif len_li <= 2:
                        # -[0]3
                        res.tzoffset = int(l[i][:2]) * 3600
                    else:
                        return None, None
                    i += 1

                    res.tzoffset *= signal

                    # Look for a timezone name between parenthesis
                    if (i + 3 < len_l and
                        info.jump(l[i]) and l[i + 1] == '(' and l[i + 3] == ')' and
                        3 <= len(l[i + 2]) <= 5 and
                        not [x for x in l[i + 2]
                             if x not in string.ascii_uppercase]):
                        # -0300 (BRST)
                        res.tzname = l[i + 2]
                        i += 4
                    continue

                # Check jumps
                if not (info.jump(l[i]) or fuzzy):
                    return None, None

                last_skipped_token_i = self._skip_token(skipped_tokens,
                                                        last_skipped_token_i, i, l)
                i += 1

            # Process year/month/day
            year, month, day = ymd.resolve_ymd(mstridx, yearfirst, dayfirst)
            if year is not None:
                res.year = year
                res.century_specified = ymd.century_specified

            if month is not None:
                res.month = month

            if day is not None:
                res.day = day

        except (IndexError, ValueError, AssertionError):
            return None, None

        if not info.validate(res):
            return None, None

        if fuzzy_with_tokens:
            return res, tuple(skipped_tokens)
        else:
            return res, None