def _format_range_context(start, stop):
    'Convert range to the "ed" format'
    # Per the diff spec at http://www.unix.org/single_unix_specification/
    beginning = start + 1     # lines start numbering with one
    length = stop - start
    if not length:
        beginning -= 1        # empty ranges begin at line just before the range
    if length <= 1:
        # return '{}'.format(beginning)
        return '%s' % (beginning)
    # return '{},{}'.format(beginning, beginning + length - 1)
    return '%s,%s' % (beginning, beginning + length - 1)