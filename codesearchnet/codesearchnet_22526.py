def get_path_extension(path):
    """
    Split file name and extension

    :type path: str|unicode
    :rtype: one str|unicode
    """
    file_path, file_ext = os.path.splitext(path)
    return file_ext.lstrip('.')