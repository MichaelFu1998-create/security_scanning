def unescape(escaped, escape_char=ESCAPE_CHAR):
    """Unescape a string escaped with `escape`
    
    escape_char must be the same as that used in the call to escape.
    """
    if isinstance(escaped, bytes):
        # always work on text
        escaped = escaped.decode('utf8')
    
    escape_pat = re.compile(re.escape(escape_char).encode('utf8') + b'([a-z0-9]{2})', re.IGNORECASE)
    buf = escape_pat.subn(_unescape_char, escaped.encode('utf8'))[0]
    return buf.decode('utf8')