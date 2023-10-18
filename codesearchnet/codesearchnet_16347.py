def findall(text):
    """Find all the timestrings within a block of text.

    >>> timestring.findall("once upon a time, about 3 weeks ago, there was a boy whom was born on august 15th at 7:20 am. epic.")
    [
     ('3 weeks ago,', <timestring.Date 2014-02-09 00:00:00 4483019280>),
     ('august 15th at 7:20 am', <timestring.Date 2014-08-15 07:20:00 4483019344>)
    ]
    """
    results = TIMESTRING_RE.findall(text)
    dates = []
    for date in results:
        if re.compile('((next|last)\s(\d+|couple(\sof))\s(weeks|months|quarters|years))|(between|from)', re.I).match(date[0]):
            dates.append((date[0].strip(), Range(date[0])))
        else:
            dates.append((date[0].strip(), Date(date[0])))
    return dates