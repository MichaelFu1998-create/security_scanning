def which(command, path=None, verbose=0, exts=None):
    """Return the full path to the first match of the given command on
    the path.

    "command" is a the name of the executable to search for.
    "path" is an optional alternate path list to search. The default it
        to use the PATH environment variable.
    "verbose", if true, will cause a 2-tuple to be returned. The second
        element is a textual description of where the match was found.
    "exts" optionally allows one to specify a list of extensions to use
        instead of the standard list for this system. This can
        effectively be used as an optimization to, for example, avoid
        stat's of "foo.vbs" when searching for "foo" and you know it is
        not a VisualBasic script but ".vbs" is on PATHEXT. This option
        is only supported on Windows.

    If no match is found for the command, a WhichError is raised.
    """
    matched = whichgen(command, path, verbose, exts)
    try:
        match = next(matched)
    except StopIteration:
        raise WhichError("Could not find '%s' on the path." % command)
    else:
        return match