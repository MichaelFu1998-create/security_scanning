def readfrom(fpath, aslines=False, errors='replace', verbose=None):
    """
    Reads (utf8) text from a file.

    Args:
        fpath (PathLike): file path
        aslines (bool): if True returns list of lines
        verbose (bool): verbosity flag

    Returns:
        str: text from fpath (this is unicode)
    """
    if verbose:
        print('Reading text file: %r ' % (fpath,))
    if not exists(fpath):
        raise IOError('File %r does not exist' % (fpath,))
    with open(fpath, 'rb') as file:
        if aslines:
            text = [line.decode('utf8', errors=errors)
                    for line in file.readlines()]
            if sys.platform.startswith('win32'):  # nocover
                # fix line endings on windows
                text = [
                    line[:-2] + '\n' if line.endswith('\r\n') else line
                    for line in text
                ]
        else:
            text = file.read().decode('utf8', errors=errors)
    return text