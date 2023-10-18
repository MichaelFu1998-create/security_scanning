def groupByContent(paths):
    """Byte-for-byte comparison on an arbitrary number of files in parallel.

    This operates by opening all files in parallel and comparing
    chunk-by-chunk. This has the following implications:

        - Reads the same total amount of data as hash comparison.
        - Performs a *lot* of disk seeks. (Best suited for SSDs)
        - Vulnerable to file handle exhaustion if used on its own.

    :param paths: List of potentially identical files.
    :type paths: iterable

    :returns: A dict mapping one path to a list of all paths (self included)
              with the same contents.

    .. todo:: Start examining the ``while handles:`` block to figure out how to
        minimize thrashing in situations where read-ahead caching is active.
        Compare savings by read-ahead to savings due to eliminating false
        positives as quickly as possible. This is a 2-variable min/max problem.

    .. todo:: Look into possible solutions for pathological cases of thousands
        of files with the same size and same pre-filter results. (File handle
        exhaustion)
    """
    handles, results = [], []

    # Silently ignore files we don't have permission to read.
    hList = []
    for path in paths:
        try:
            hList.append((path, open(path, 'rb'), ''))
        except IOError:
            pass  # TODO: Verbose-mode output here.
    handles.append(hList)

    while handles:
        # Process more blocks.
        more, done = compareChunks(handles.pop(0))

        # Add the results to the top-level lists.
        handles.extend(more)
        results.extend(done)

    # Keep the same API as the others.
    return dict((x[0], x) for x in results)