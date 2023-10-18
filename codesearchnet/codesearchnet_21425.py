def _unicode(string):
    """Try to convert a string to unicode using different encodings"""
    for encoding in ['utf-8', 'latin1']:
        try:
            result = unicode(string, encoding)
            return result
        except UnicodeDecodeError:
            pass
    result = unicode(string, 'utf-8', 'replace')
    return result