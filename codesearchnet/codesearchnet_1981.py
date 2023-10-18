def formatwarning(message, category, filename, lineno, line=None):
    """Function to format a warning the standard way."""
    try:
        unicodetype = unicode
    except NameError:
        unicodetype = ()
    try:
        message = str(message)
    except UnicodeEncodeError:
        pass
    s =  "%s: %s: %s\n" % (lineno, category.__name__, message)
    line = linecache.getline(filename, lineno) if line is None else line
    if line:
        line = line.strip()
        if isinstance(s, unicodetype) and isinstance(line, str):
            line = unicode(line, 'latin1')
        s += "  %s\n" % line
    if isinstance(s, unicodetype) and isinstance(filename, str):
        enc = sys.getfilesystemencoding()
        if enc:
            try:
                filename = unicode(filename, enc)
            except UnicodeDecodeError:
                pass
    s = "%s:%s" % (filename, s)
    return s