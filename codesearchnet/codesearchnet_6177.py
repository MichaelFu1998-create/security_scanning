def pop_path2(path):
    """Return '/a/b/c' -> ('a', 'b', '/c')."""
    if path in ("", "/"):
        return ("", "", "")
    first, rest = pop_path(path)
    second, rest = pop_path(rest)
    return (first, second, "/" + rest)