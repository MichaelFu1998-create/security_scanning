def ReplaceInFile(filename, old, new, encoding=None):
    '''
    Replaces all occurrences of "old" by "new" in the given file.

    :param unicode filename:
        The name of the file.

    :param unicode old:
        The string to search for.

    :param unicode new:
        Replacement string.

    :return unicode:
        The new contents of the file.
    '''
    contents = GetFileContents(filename, encoding=encoding)
    contents = contents.replace(old, new)
    CreateFile(filename, contents, encoding=encoding)
    return contents