def abspath(cur_file, parent=0) -> str:
    """
    Absolute path

    Args:
        cur_file: __file__ or file or path str
        parent: level of parent to look for

    Returns:
        str
    """
    file_path = os.path.abspath(cur_file).replace('\\', '/')
    if os.path.isdir(file_path) and parent == 0: return file_path
    adj = 1 - os.path.isdir(file_path)
    return '/'.join(file_path.split('/')[:-(parent + adj)])