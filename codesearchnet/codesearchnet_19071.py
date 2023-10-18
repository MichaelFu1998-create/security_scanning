def unicodevalues_asstring(values):
    """ Return string with unicodenames (unless that is disabled) """
    if not os.environ.get('DISABLE_UNAMES'):
        return map(lambda x: '%s' % format(x).strip(), values)
    return map(lambda x: u'U+%04x %s' % (x, unichr(x)), sorted(values))