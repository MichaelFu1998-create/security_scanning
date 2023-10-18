def parse_python_file(filepath):
    """
    Retrieves the AST of the specified file.

    This function performs simple caching so that the same file isn't read or
    parsed more than once per process.

    :param filepath: the file to parse
    :type filepath: str
    :returns: ast.AST
    """

    with _AST_CACHE_LOCK:
        if filepath not in _AST_CACHE:
            source = read_file(filepath)
            _AST_CACHE[filepath] = ast.parse(source, filename=filepath)
    return _AST_CACHE[filepath]