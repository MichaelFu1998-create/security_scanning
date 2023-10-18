def find_dupes(paths, exact=False, ignores=None, min_size=0):
    """High-level code to walk a set of paths and find duplicate groups.

    :param exact: Whether to compare file contents by hash or by reading
                  chunks in parallel.
    :type exact: :class:`~__builtins__.bool`

    :param paths: See :meth:`~fastdupes.getPaths`
    :param ignores: See :meth:`~fastdupes.getPaths`
    :param min_size: See :meth:`~fastdupes.sizeClassifier`

    :returns: A list of groups of files with identical contents
    :rtype: ``[[path, ...], [path, ...]]``
    """
    groups = {'': getPaths(paths, ignores)}
    groups = groupBy(groups, sizeClassifier, 'sizes', min_size=min_size)

    # This serves one of two purposes depending on run-mode:
    # - Minimize number of files checked by full-content comparison (hash)
    # - Minimize chances of file handle exhaustion and limit seeking (exact)
    groups = groupBy(groups, hashClassifier, 'header hashes', limit=HEAD_SIZE)

    if exact:
        groups = groupBy(groups, groupByContent, fun_desc='contents')
    else:
        groups = groupBy(groups, hashClassifier, fun_desc='hashes')

    return groups