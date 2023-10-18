def CreateFile(filename, contents, eol_style=EOL_STYLE_NATIVE, create_dir=True, encoding=None, binary=False):
    '''
    Create a file with the given contents.

    :param unicode filename:
        Filename and path to be created.

    :param unicode contents:
        The file contents as a string.

    :type eol_style: EOL_STYLE_XXX constant
    :param eol_style:
        Replaces the EOL by the appropriate EOL depending on the eol_style value.
        Considers that all content is using only "\n" as EOL.

    :param bool create_dir:
        If True, also creates directories needed in filename's path

    :param unicode encoding:
        Target file's content encoding. Defaults to sys.getfilesystemencoding()
        Ignored if `binary` = True

    :param bool binary:
        If True, file is created in binary mode. In this case, `contents` must be `bytes` and not
        `unicode`

    :return unicode:
        Returns the name of the file created.

    :raises NotImplementedProtocol:
        If file protocol is not local or FTP

    :raises ValueError:
        If trying to mix unicode `contents` without `encoding`, or `encoding` without
        unicode `contents`

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    # Lots of checks when writing binary files
    if binary:
        if isinstance(contents, six.text_type):
            raise TypeError('contents must be str (bytes) when binary=True')
    else:
        if not isinstance(contents, six.text_type):
            raise TypeError('contents must be unicode when binary=False')

        # Replaces eol on each line by the given eol_style.
        contents = _HandleContentsEol(contents, eol_style)

        # Encode string and pretend we are using binary to prevent 'open' from automatically
        # changing Eols
        encoding = encoding or sys.getfilesystemencoding()
        contents = contents.encode(encoding)
        binary = True

    # If asked, creates directory containing file
    if create_dir:
        dirname = os.path.dirname(filename)
        if dirname:
            CreateDirectory(dirname)

    from six.moves.urllib.parse import urlparse
    filename_url = urlparse(filename)

    # Handle local
    if _UrlIsLocal(filename_url):
        # Always writing as binary (see handling above)
        with open(filename, 'wb') as oss:
            oss.write(contents)

    # Handle FTP
    elif filename_url.scheme == 'ftp':
        # Always writing as binary (see handling above)
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(directory_url.scheme)
    else:
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(filename_url.scheme)

    return filename