def _restore_path(table):
    """Restore resource's path and name from storage's table.

    Args:
        table (str): table name

    Returns:
        (str, str): resource path and name

    """
    name = None
    splited = table.split('___')
    path = splited[0]
    if len(splited) == 2:
        name = splited[1]
    path = path.replace('__', os.path.sep)
    path += '.csv'
    return path, name