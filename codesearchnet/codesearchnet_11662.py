def which(program):
    ''' look for "program" in PATH (respecting PATHEXT), and return the path to
        it, or None if it was not found
    '''
    # current directory / absolute paths:
    if os.path.exists(program) and os.access(program, os.X_OK):
        return program
    # PATH:
    for path in os.environ['PATH'].split(os.pathsep):
        # path variables may be quoted:
        path = path.strip('"')
        for ext in os.environ.get('PATHEXT', '').split(os.pathsep):
            progpath = os.path.join(path, program + ext)
            if os.path.exists(progpath) and os.access(progpath, os.X_OK):
                return progpath
    # not found
    return None