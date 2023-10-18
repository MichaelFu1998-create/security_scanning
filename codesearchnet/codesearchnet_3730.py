def log(s, header='', file=sys.stderr, nl=1, **kwargs):
    """Log the given output to stderr if and only if we are in
    verbose mode.

    If we are not in verbose mode, this is a no-op.
    """
    # Sanity check: If we are not in verbose mode, this is a no-op.
    if not settings.verbose:
        return

    # Construct multi-line string to stderr if header is provided.
    if header:
        word_arr = s.split(' ')
        multi = []
        word_arr.insert(0, '%s:' % header.upper())
        i = 0
        while i < len(word_arr):
            to_add = ['***']
            count = 3
            while count <= 79:
                count += len(word_arr[i]) + 1
                if count <= 79:
                    to_add.append(word_arr[i])
                    i += 1
                    if i == len(word_arr):
                        break
            # Handle corner case of extra-long word longer than 75 characters.
            if len(to_add) == 1:
                to_add.append(word_arr[i])
                i += 1
            if i != len(word_arr):
                count -= len(word_arr[i]) + 1
            to_add.append('*' * (78 - count))
            multi.append(' '.join(to_add))
        s = '\n'.join(multi)
        lines = len(multi)
    else:
        lines = 1

    # If `nl` is an int greater than the number of rows of a message,
    # add the appropriate newlines to the output.
    if isinstance(nl, int) and nl > lines:
        s += '\n' * (nl - lines)

    # Output to stderr.
    return secho(s, file=file, **kwargs)