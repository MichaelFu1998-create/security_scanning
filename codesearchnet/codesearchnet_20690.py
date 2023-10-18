def recursive_dir_match(folder_path, regex=''):
    """
    Returns absolute paths of folders that match the regex within folder_path and
    all its children folders.

    Note: The regex matching is done using the match function
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
        outlist.extend([op.join(root, f) for f in dirs
                        if re.match(regex, f)])

    return outlist