def compareChunks(handles, chunk_size=CHUNK_SIZE):
    """Group a list of file handles based on equality of the next chunk of
    data read from them.

    :param handles: A list of open handles for file-like objects with
        otentially-identical contents.
    :param chunk_size: The amount of data to read from each handle every time
        this function is called.

    :returns: Two lists of lists:

        * Lists to be fed back into this function individually
        * Finished groups of duplicate paths. (including unique files as
          single-file lists)

    :rtype: ``(list, list)``

    .. attention:: File handles will be closed when no longer needed
    .. todo:: Discard chunk contents immediately once they're no longer needed
    """
    chunks = [(path, fh, fh.read(chunk_size)) for path, fh, _ in handles]
    more, done = [], []

    # While there are combinations not yet tried...
    while chunks:
        # Compare the first chunk to all successive chunks
        matches, non_matches = [chunks[0]], []
        for chunk in chunks[1:]:
            if matches[0][2] == chunk[2]:
                matches.append(chunk)
            else:
                non_matches.append(chunk)
        # Check for EOF or obviously unique files
        if len(matches) == 1 or matches[0][2] == "":
            for x in matches:
                x[1].close()
            done.append([x[0] for x in matches])
        else:
            more.append(matches)
        chunks = non_matches

    return more, done