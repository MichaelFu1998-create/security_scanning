def _cull(potential, matches, verbose=0):
    """Cull inappropriate matches. Possible reasons:
        - a duplicate of a previous match
        - not a disk file
        - not executable (non-Windows)
    If 'potential' is approved it is returned and added to 'matches'.
    Otherwise, None is returned.
    """
    for match in matches: # don't yield duplicates
        if _samefile(potential[0], match[0]):
            if verbose:
                sys.stderr.write("duplicate: %s (%s)\n" % potential)
            return None

    if not stat.S_ISREG(os.stat(potential[0]).st_mode):
        if verbose:
            sys.stderr.write("not a regular file: %s (%s)\n" % potential)
    elif not os.access(potential[0], os.X_OK):
        if verbose:
            sys.stderr.write("no executable access: %s (%s)\n" % potential)
    else:
        matches.append(potential)
        return potential

    return None