def table(*columns, **kwargs):
    """
    format columned data so we can easily print it out on a console, this just takes
    columns of data and it will format it into properly aligned columns, it's not
    fancy, but it works for most type of strings that I need it for, like server name
    lists.

    other formatting options:
        http://stackoverflow.com/a/8234511/5006

    other packages that probably do this way better:
        https://stackoverflow.com/a/26937531/5006

    :Example:
        >>> echo.table([(1, 2), (3, 4), (5, 6), (7, 8), (9, 0)])
        1  2
        3  4
        5  6
        7  8
        9  0
        >>> echo.table([1, 3, 5, 7, 9], [2, 4, 6, 8, 0])
        1  2
        3  4
        5  6
        7  8
        9  0

    :param *columns: can either be a list of rows or multiple lists representing each
        column in the table
    :param **kwargs: dict
        prefix -- string -- what you want before each row (eg, a tab)
        buf_count -- integer -- how many spaces between longest col value and its neighbor
        headers -- list -- the headers you want, must match column count
        widths -- list -- the widths of each column you want to use, this doesn't have
            to match column count, so you can do something like [0, 5] to set the
            width of the second column
        width -- int -- similar to widths except it will set this value for all columns
    """
    ret = []
    prefix = kwargs.get('prefix', '')
    buf_count = kwargs.get('buf_count', 2)
    if len(columns) == 1:
        columns = list(columns[0])
    else:
        # without the list the zip iterator gets spent, I'm sure I can make this
        # better
        columns = list(zip(*columns))

    headers = kwargs.get("headers", [])
    if headers:
        columns.insert(0, headers)

    # we have to go through all the rows and calculate the length of each
    # column of each row
    widths = kwargs.get("widths", [])
    row_counts = Counter()
    for i in range(len(widths)):
        row_counts[i] = int(widths[i])

    width = int(kwargs.get("width", 0))
    for row in columns:
        for i, c in enumerate(row):
            if isinstance(c, basestring):
                cl = len(c)
            else:
                cl = len(str(c))
            if cl > row_counts[i]:
                row_counts[i] = cl

    width = int(kwargs.get("width", 0))
    if width:
        for i in row_counts:
            if row_counts[i] < width:
                row_counts[i] = width

    # actually go through and format each row
    def colstr(c):
        if isinstance(c, basestring): return c
        return str(c)

    def rowstr(row, prefix, row_counts):
        row_format = prefix
        cols = list(map(colstr, row))
        for i in range(len(row_counts)):
            c = cols[i]
            # build the format string for each row, we use the row_counts found
            # above to decide how much padding each column should get
            # https://stackoverflow.com/a/9536084/5006
            if re.match(r"^\d+(?:\.\d+)?$", c):
                if i == 0:
                    row_format += "{:>" + str(row_counts[i]) + "}"
                else:
                    row_format += "{:>" + str(row_counts[i] + buf_count) + "}"
            else:
                row_format += "{:<" + str(row_counts[i] + buf_count) + "}"

        return row_format.format(*cols)

    for row in columns:
        ret.append(rowstr(row, prefix, row_counts))

    out(os.linesep.join(ret))