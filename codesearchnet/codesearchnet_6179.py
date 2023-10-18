def split_namespace(clarkName):
    """Return (namespace, localname) tuple for a property name in Clark Notation.

    Namespace defaults to ''.
    Example:
    '{DAV:}foo'  -> ('DAV:', 'foo')
    'bar'  -> ('', 'bar')
    """
    if clarkName.startswith("{") and "}" in clarkName:
        ns, localname = clarkName.split("}", 1)
        return (ns[1:], localname)
    return ("", clarkName)