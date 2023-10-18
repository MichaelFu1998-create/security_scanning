def shift_path(script_name, path_info):
    """Return ('/a', '/b/c') -> ('b', '/a/b', 'c')."""
    segment, rest = pop_path(path_info)
    return (segment, join_uri(script_name.rstrip("/"), segment), rest.rstrip("/"))