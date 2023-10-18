def groupBy(groups_in, classifier, fun_desc='?', keep_uniques=False,
            *args, **kwargs):
    """Subdivide groups of paths according to a function.

    :param groups_in: Grouped sets of paths.
    :type groups_in: :class:`~__builtins__.dict` of iterables

    :param classifier: Function to group a list of paths by some attribute.
    :type classifier: ``function(list, *args, **kwargs) -> str``

    :param fun_desc: Human-readable term for what the classifier operates on.
        (Used in log messages)
    :type fun_desc: :class:`~__builtins__.str`

    :param keep_uniques: If ``False``, discard groups with only one member.
    :type keep_uniques: :class:`~__builtins__.bool`


    :returns: A dict mapping classifier keys to groups of matches.
    :rtype: :class:`~__builtins__.dict`


    :attention: Grouping functions generally use a :class:`~__builtins__.set`
        ``groups`` as extra protection against accidentally counting a given
        file twice. (Complimentary to use of :func:`os.path.realpath` in
        :func:`~fastdupes.getPaths`)

    .. todo:: Find some way to bring back the file-by-file status text
    """
    groups, count, group_count = {}, 0, len(groups_in)
    for pos, paths in enumerate(groups_in.values()):
        out.write("Subdividing group %d of %d by %s... (%d files examined, %d "
                  "in current group)" % (
                      pos + 1, group_count, fun_desc, count, len(paths)
                  ))

        for key, group in classifier(paths, *args, **kwargs).items():
            groups.setdefault(key, set()).update(group)
            count += len(group)

    if not keep_uniques:
        # Return only the groups with more than one file.
        groups = dict([(x, groups[x]) for x in groups if len(groups[x]) > 1])

    out.write("Found %s sets of files with identical %s. (%d files examined)"
              % (len(groups), fun_desc, count), newline=True)
    return groups