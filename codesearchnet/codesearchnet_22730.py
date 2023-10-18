def GetFileContents(filename, binary=False, encoding=None, newline=None):
    '''
    Reads a file and returns its contents. Works for both local and remote files.

    :param unicode filename:

    :param bool binary:
        If True returns the file as is, ignore any EOL conversion.

    :param unicode encoding:
        File's encoding. If not None, contents obtained from file will be decoded using this
        `encoding`.

    :param None|''|'\n'|'\r'|'\r\n' newline:
        Controls universal newlines.
        See 'io.open' newline parameter documentation for more details.

    :returns str|unicode:
        The file's contents.
        Returns unicode string when `encoding` is not None.

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    source_file = OpenFile(filename, binary=binary, encoding=encoding, newline=newline)
    try:
        contents = source_file.read()
    finally:
        source_file.close()

    return contents