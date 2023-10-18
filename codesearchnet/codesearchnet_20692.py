def recursive_find_search(folder_path, regex=''):
    """
    Returns absolute paths of files that match the regex within file_dir and
    all its children folders.

    Note: The regex matching is done using the search function
    of the re module.

    Parameters
    ----------
    folder_path: string

    regex: string

    Returns
    -------
    A list of strings.

    """
    outlist = []
    for root, dirs, files in os.walk(folder_path):
        outlist.extend([op.join(root, f) for f in files
                        if re.search(regex, f)])

    return outlist