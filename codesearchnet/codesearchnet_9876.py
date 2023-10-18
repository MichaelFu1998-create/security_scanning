def _convert_path(path, name):
    """Convert resource's path and name to storage's table name.

    Args:
        path (str): resource path
        name (str): resource name

    Returns:
        str: table name

    """
    table = os.path.splitext(path)[0]
    table = table.replace(os.path.sep, '__')
    if name is not None:
        table = '___'.join([table, name])
    table = re.sub('[^0-9a-zA-Z_]+', '_', table)
    table = table.lower()
    return table