def find_executables(path):
    """ Find executables in a path.

    Searches executables in a directory excluding some know commands
    unusable with GromacsWrapper.

    :param path: dirname to search for
    :return: list of executables
    """
    execs = []
    for exe in os.listdir(path):
        fullexe = os.path.join(path, exe)
        if (os.access(fullexe, os.X_OK) and not os.path.isdir(fullexe) and
             exe not in ['GMXRC', 'GMXRC.bash', 'GMXRC.csh', 'GMXRC.zsh',
                         'demux.pl', 'xplor2gmx.pl']):
            execs.append(exe)
    return execs