def write_to_file(file_path, contents, encoding="utf-8"):
    """
    Write helper method

    :type file_path: str|unicode
    :type contents: str|unicode
    :type encoding: str|unicode
    """
    with codecs.open(file_path, "w", encoding) as f:
        f.write(contents)