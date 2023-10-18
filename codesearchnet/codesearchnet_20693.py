def iter_recursive_find(folder_path, *regex):
    """
    Returns absolute paths of files that match the regexs within folder_path and
    all its children folders.

    This is an iterator function that will use yield to return each set of
    file_paths in one iteration.

    Will only return value if all the strings in regex match a file name.

    Note: The regex matching is done using the search function
    of the re module.

    Parameters
    ----------
    folder_path: string

    regex: strings

    Returns
    -------
    A list of strings.
    """
    for root, dirs, files in os.walk(folder_path):
        if len(files) > 0:
            outlist = []
            for f in files:
                for reg in regex:
                    if re.search(reg, f):
                        outlist.append(op.join(root, f))
            if len(outlist) == len(regex):
                yield outlist