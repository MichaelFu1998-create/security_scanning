def GetFileLines(filename, newline=None, encoding=None):
    '''
    Reads a file and returns its contents as a list of lines. Works for both local and remote files.

    :param unicode filename:

    :param None|''|'\n'|'\r'|'\r\n' newline:
        Controls universal newlines.
        See 'io.open' newline parameter documentation for more details.

    :param unicode encoding:
        File's encoding. If not None, contents obtained from file will be decoded using this
        `encoding`.

    :returns list(unicode):
        The file's lines

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    return GetFileContents(
        filename,
        binary=False,
        encoding=encoding,
        newline=newline,
    ).split('\n')