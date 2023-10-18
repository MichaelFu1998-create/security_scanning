def get_file_list(file_dir, regex=''):
    """
    Creates a list of files that match the search_regex within file_dir.
    The list of files will have file_dir as path prefix.

    Parameters
    ----------
    @param file_dir:

    @param search_regex:

    Returns:
    --------
    List of paths to files that match the search_regex
    """
    file_list = os.listdir(file_dir)
    file_list.sort()

    if regex:
        file_list = search_list(file_list, regex)

    file_list = [op.join(file_dir, fname) for fname in file_list]

    return file_list