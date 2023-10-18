def _parse_dir(directory, relpath):
    """
    Return a list of :class:`_PyconfigCall` from recursively parsing
    `directory`.

    :param directory: Directory to walk looking for python files
    :param relpath: Path to make filenames relative to
    :type directory: str
    :type relpath: str

    """
    relpath = os.path.dirname(relpath)
    pyconfig_calls = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if not filename.endswith('.py'):
                continue
            filename = os.path.join(root, filename)
            pyconfig_calls.extend(_parse_file(filename, relpath))

    return pyconfig_calls