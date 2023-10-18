def whichgen(command, path=None, verbose=0, exts=None): # pylint: disable=too-many-branches, too-many-statements
    """Return a generator of full paths to the given command.

    "command" is a the name of the executable to search for.
    "path" is an optional alternate path list to search. The default it
        to use the PATH environment variable.
    "verbose", if true, will cause a 2-tuple to be returned for each
        match. The second element is a textual description of where the
        match was found.
    "exts" optionally allows one to specify a list of extensions to use
        instead of the standard list for this system. This can
        effectively be used as an optimization to, for example, avoid
        stat's of "foo.vbs" when searching for "foo" and you know it is
        not a VisualBasic script but ".vbs" is on PATHEXT. This option
        is only supported on Windows.

    This method returns a generator which yields either full paths to
    the given command or, if verbose, tuples of the form (<path to
    command>, <where path found>).
    """
    matches = []
    if path is None:
        using_given_path = 0
        path = os.environ.get("PATH", "").split(os.pathsep)
        if sys.platform.startswith("win"):
            path.insert(0, os.curdir)  # implied by Windows shell
    else:
        using_given_path = 1

    # Windows has the concept of a list of extensions (PATHEXT env var).
    if sys.platform.startswith("win"):
        if exts is None:
            exts = os.environ.get("PATHEXT", "").split(os.pathsep)
            # If '.exe' is not in exts then obviously this is Win9x and
            # or a bogus PATHEXT, then use a reasonable default.
            for ext in exts:
                if ext.lower() == ".exe":
                    break
            else:
                exts = ['.COM', '.EXE', '.BAT']
        elif not isinstance(exts, list):
            raise TypeError("'exts' argument must be a list or None")
    else:
        if exts is not None:
            raise WhichError("'exts' argument is not supported on platform '%s'" % sys.platform)
        exts = []

    # File name cannot have path separators because PATH lookup does not
    # work that way.
    if os.sep in command or os.altsep and os.altsep in command:
        pass
    else:
        for i, dir_name in enumerate(path):
            # On windows the dir_name *could* be quoted, drop the quotes
            if sys.platform.startswith("win") and len(dir_name) >= 2 and dir_name[0] == '"' and dir_name[-1] == '"':
                dir_name = dir_name[1:-1]
            for ext in ['']+exts:
                abs_name = os.path.abspath(os.path.normpath(os.path.join(dir_name, command+ext)))
                if os.path.isfile(abs_name):
                    if using_given_path:
                        from_where = "from given path element %d" % i
                    elif not sys.platform.startswith("win"):
                        from_where = "from PATH element %d" % i
                    elif i == 0:
                        from_where = "from current directory"
                    else:
                        from_where = "from PATH element %d" % (i-1)
                    match = _cull((abs_name, from_where), matches, verbose)
                    if match:
                        if verbose:
                            yield match
                        else:
                            yield match[0]
        match = _get_registered_executable(command)
        if match is not None:
            match = _cull(match, matches, verbose)
            if match:
                if verbose:
                    yield match
                else:
                    yield match[0]