def _format_range_unified(start, stop):
    'Convert range to the "ed" format'
    # Per the diff spec at http://www.unix.org/single_unix_specification/
    beginning = start + 1     # lines start numbering with one
    length = stop - start
    if length == 1:
        # return '{}'.format(beginning)
        return '%s' % (beginning)
    if not length:
        beginning -= 1        # empty ranges begin at line just before the range
    return '%s,%s' % (beginning, length)