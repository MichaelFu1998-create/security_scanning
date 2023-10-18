def _guess_quote_and_delimiter(self, data, delimiters):
        """
        Looks for text enclosed between two identical quotes
        (the probable quotechar) which are preceded and followed
        by the same character (the probable delimiter).
        For example:
                         ,'some text',
        The quote with the most wins, same with the delimiter.
        If there is no quotechar the delimiter can't be determined
        this way.
        """

        matches = []
        for restr in ('(?P<delim>[^\w\n"\'])(?P<space> ?)(?P<quote>["\']).*?(?P=quote)(?P=delim)', # ,".*?",
                      '(?:^|\n)(?P<quote>["\']).*?(?P=quote)(?P<delim>[^\w\n"\'])(?P<space> ?)',   #  ".*?",
                      '(?P<delim>>[^\w\n"\'])(?P<space> ?)(?P<quote>["\']).*?(?P=quote)(?:$|\n)',  # ,".*?"
                      '(?:^|\n)(?P<quote>["\']).*?(?P=quote)(?:$|\n)'):                            #  ".*?" (no delim, no space)
            regexp = re.compile(restr, re.DOTALL | re.MULTILINE)
            matches = regexp.findall(data)
            if matches:
                break

        if not matches:
            # (quotechar, doublequote, delimiter, skipinitialspace)
            return ('', False, None, 0)
        quotes = {}
        delims = {}
        spaces = 0
        for m in matches:
            n = regexp.groupindex['quote'] - 1
            key = m[n]
            if key:
                quotes[key] = quotes.get(key, 0) + 1
            try:
                n = regexp.groupindex['delim'] - 1
                key = m[n]
            except KeyError:
                continue
            if key and (delimiters is None or key in delimiters):
                delims[key] = delims.get(key, 0) + 1
            try:
                n = regexp.groupindex['space'] - 1
            except KeyError:
                continue
            if m[n]:
                spaces += 1

        quotechar = reduce(lambda a, b, quotes = quotes:
                           (quotes[a] > quotes[b]) and a or b, quotes.keys())

        if delims:
            delim = reduce(lambda a, b, delims = delims:
                           (delims[a] > delims[b]) and a or b, delims.keys())
            skipinitialspace = delims[delim] == spaces
            if delim == '\n': # most likely a file with a single column
                delim = ''
        else:
            # there is *no* delimiter, it's a single column of quoted data
            delim = ''
            skipinitialspace = 0

        # if we see an extra quote between delimiters, we've got a
        # double quoted format
        dq_regexp = re.compile(
                               r"((%(delim)s)|^)\W*%(quote)s[^%(delim)s\n]*%(quote)s[^%(delim)s\n]*%(quote)s\W*((%(delim)s)|$)" % \
                               {'delim':re.escape(delim), 'quote':quotechar}, re.MULTILINE)



        if dq_regexp.search(data):
            doublequote = True
        else:
            doublequote = False

        return (quotechar, doublequote, delim, skipinitialspace)