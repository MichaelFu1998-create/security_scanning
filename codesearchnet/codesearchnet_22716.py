def CopyFile(source_filename, target_filename, override=True, md5_check=False, copy_symlink=True):
    '''
    Copy a file from source to target.

    :param  source_filename:
        @see _DoCopyFile

    :param  target_filename:
        @see _DoCopyFile

    :param bool md5_check:
        If True, checks md5 files (of both source and target files), if they match, skip this copy
        and return MD5_SKIP

        Md5 files are assumed to be {source, target} + '.md5'

        If any file is missing (source, target or md5), the copy will always be made.

    :param  copy_symlink:
        @see _DoCopyFile

    :raises FileAlreadyExistsError:
        If target_filename already exists, and override is False

    :raises NotImplementedProtocol:
        If file protocol is not accepted

        Protocols allowed are:
            source_filename: local, ftp, http
            target_filename: local, ftp

    :rtype: None | MD5_SKIP
    :returns:
        MD5_SKIP if the file was not copied because there was a matching .md5 file

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    from ._exceptions import FileNotFoundError

    # Check override
    if not override and Exists(target_filename):
        from ._exceptions import FileAlreadyExistsError
        raise FileAlreadyExistsError(target_filename)

    # Don't do md5 check for md5 files themselves.
    md5_check = md5_check and not target_filename.endswith('.md5')

    # If we enabled md5 checks, ignore copy of files that haven't changed their md5 contents.
    if md5_check:
        source_md5_filename = source_filename + '.md5'
        target_md5_filename = target_filename + '.md5'
        try:
            source_md5_contents = GetFileContents(source_md5_filename)
        except FileNotFoundError:
            source_md5_contents = None

        try:
            target_md5_contents = GetFileContents(target_md5_filename)
        except FileNotFoundError:
            target_md5_contents = None

        if source_md5_contents is not None and \
           source_md5_contents == target_md5_contents and \
           Exists(target_filename):
            return MD5_SKIP

    # Copy source file
    _DoCopyFile(source_filename, target_filename, copy_symlink=copy_symlink)

    # If we have a source_md5, but no target_md5, create the target_md5 file
    if md5_check and source_md5_contents is not None and source_md5_contents != target_md5_contents:
        CreateFile(target_md5_filename, source_md5_contents)