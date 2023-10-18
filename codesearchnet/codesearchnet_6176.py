def pop_path(path):
    """Return '/a/b/c' -> ('a', '/b/c')."""
    if path in ("", "/"):
        return ("", "")
    assert path.startswith("/")
    first, _sep, rest = path.lstrip("/").partition("/")
    return (first, "/" + rest)