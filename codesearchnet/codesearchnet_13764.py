def delete_dupes(groups, prefer_list=None, interactive=True, dry_run=False):
    """Code to handle the :option:`--delete` command-line option.

    :param groups: A list of groups of paths.
    :type groups: iterable

    :param prefer_list: A whitelist to be compiled by
        :func:`~fastdupes.multiglob_compile` and used to skip some prompts.

    :param interactive: If ``False``, assume the user wants to keep all copies
        when a prompt would otherwise be displayed.
    :type interactive: :class:`~__builtins__.bool`

    :param dry_run: If ``True``, only pretend to delete files.
    :type dry_run: :class:`~__builtins__.bool`

    .. todo:: Add a secondary check for symlinks for safety.
    """
    prefer_list = prefer_list or []
    prefer_re = multiglob_compile(prefer_list, prefix=True)

    for pos, group in enumerate(groups.values()):
        preferred = [x for x in group if prefer_re.match(x)]
        pruneList = [x for x in group if x not in preferred]
        if not preferred:
            if interactive:
                pruneList = pruneUI(group, pos + 1, len(groups))
                preferred = [x for x in group if x not in pruneList]
            else:
                preferred, pruneList = pruneList, []

        assert preferred  # Safety check
        for path in pruneList:
            print "Removing %s" % path
            if not dry_run:
                os.remove(path)