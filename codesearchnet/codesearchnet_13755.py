def getPaths(roots, ignores=None):
    """
    Recursively walk a set of paths and return a listing of contained files.

    :param roots: Relative or absolute paths to files or folders.
    :type roots: :class:`~__builtins__.list` of :class:`~__builtins__.str`

    :param ignores: A list of :py:mod:`fnmatch` globs to avoid walking and
        omit from results
    :type ignores: :class:`~__builtins__.list` of :class:`~__builtins__.str`

    :returns: Absolute paths to only files.
    :rtype: :class:`~__builtins__.list` of :class:`~__builtins__.str`

    .. todo:: Try to optimize the ignores matching. Running a regex on every
       filename is a fairly significant percentage of the time taken according
       to the profiler.
    """
    paths, count, ignores = [], 0, ignores or []

    # Prepare the ignores list for most efficient use
    ignore_re = multiglob_compile(ignores, prefix=False)

    for root in roots:
        # For safety, only use absolute, real paths.
        root = os.path.realpath(root)

        # Handle directly-referenced filenames properly
        # (And override ignores to "do as I mean, not as I say")
        if os.path.isfile(root):
            paths.append(root)
            continue

        for fldr in os.walk(root):
            out.write("Gathering file paths to compare... (%d files examined)"
                      % count)

            # Don't even descend into IGNOREd directories.
            for subdir in fldr[1]:
                dirpath = os.path.join(fldr[0], subdir)
                if ignore_re.match(dirpath):
                    fldr[1].remove(subdir)

            for filename in fldr[2]:
                filepath = os.path.join(fldr[0], filename)
                if ignore_re.match(filepath):
                    continue  # Skip IGNOREd files.

                paths.append(filepath)
                count += 1

    out.write("Found %s files to be compared for duplication." % (len(paths)),
              newline=True)
    return paths