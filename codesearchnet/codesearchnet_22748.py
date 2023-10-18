def FindFiles(dir_, in_filters=None, out_filters=None, recursive=True, include_root_dir=True, standard_paths=False):
    '''
    Searches for files in a given directory that match with the given patterns.

    :param str dir_: the directory root, to search the files.
    :param list(str) in_filters: a list with patterns to match (default = all). E.g.: ['*.py']
    :param list(str) out_filters: a list with patterns to ignore (default = none). E.g.: ['*.py']
    :param bool recursive: if True search in subdirectories, otherwise, just in the root.
    :param bool include_root_dir: if True, includes the directory being searched in the returned paths
    :param bool standard_paths: if True, always uses unix path separators "/"
    :return list(str):
        A list of strings with the files that matched (with the full path in the filesystem).
    '''
    # all files
    if in_filters is None:
        in_filters = ['*']

    if out_filters is None:
        out_filters = []

    result = []

    # maintain just files that don't have a pattern that match with out_filters
    # walk through all directories based on dir
    for dir_root, directories, filenames in os.walk(dir_):

        for i_directory in directories[:]:
            if MatchMasks(i_directory, out_filters):
                directories.remove(i_directory)

        for filename in directories + filenames:
            if MatchMasks(filename, in_filters) and not MatchMasks(filename, out_filters):
                result.append(os.path.join(dir_root, filename))

        if not recursive:
            break

    if not include_root_dir:
        # Remove root dir from all paths
        dir_prefix = len(dir_) + 1
        result = [file[dir_prefix:] for file in result]

    if standard_paths:
        result = map(StandardizePath, result)

    return result