def AppendToFile(filename, contents, eol_style=EOL_STYLE_NATIVE, encoding=None, binary=False):
    '''
    Appends content to a local file.

    :param unicode filename:

    :param unicode contents:

    :type eol_style: EOL_STYLE_XXX constant
    :param eol_style:
        Replaces the EOL by the appropriate EOL depending on the eol_style value.
        Considers that all content is using only "\n" as EOL.

    :param unicode encoding:
        Target file's content encoding.
        Defaults to sys.getfilesystemencoding()

    :param bool binary:
        If True, content is appended in binary mode. In this case, `contents` must be `bytes` and not
        `unicode`

    :raises NotImplementedForRemotePathError:
        If trying to modify a non-local path

    :raises ValueError:
        If trying to mix unicode `contents` without `encoding`, or `encoding` without
        unicode `contents`
    '''
    _AssertIsLocal(filename)

    assert isinstance(contents, six.text_type) ^ binary, 'Must always receive unicode contents, unless binary=True'

    if not binary:
        # Replaces eol on each line by the given eol_style.
        contents = _HandleContentsEol(contents, eol_style)

        # Handle encoding here, and always write in binary mode. We can't use io.open because it
        # tries to do its own line ending handling.
        contents = contents.encode(encoding or sys.getfilesystemencoding())

    oss = open(filename, 'ab')
    try:
        oss.write(contents)
    finally:
        oss.close()