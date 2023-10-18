def CopyFiles(source_dir, target_dir, create_target_dir=False, md5_check=False):
    '''
    Copy files from the given source to the target.

    :param unicode source_dir:
        A filename, URL or a file mask.
        Ex.
            x:\coilib50
            x:\coilib50\*
            http://server/directory/file
            ftp://server/directory/file


    :param unicode target_dir:
        A directory or an URL
        Ex.
            d:\Temp
            ftp://server/directory

    :param bool create_target_dir:
        If True, creates the target path if it doesn't exists.

    :param bool md5_check:
        .. seealso:: CopyFile

    :raises DirectoryNotFoundError:
        If target_dir does not exist, and create_target_dir is False

    .. seealso:: CopyFile for documentation on accepted protocols

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    import fnmatch

    # Check if we were given a directory or a directory with mask
    if IsDir(source_dir):
        # Yes, it's a directory, copy everything from it
        source_mask = '*'
    else:
        # Split directory and mask
        source_dir, source_mask = os.path.split(source_dir)

    # Create directory if necessary
    if not IsDir(target_dir):
        if create_target_dir:
            CreateDirectory(target_dir)
        else:
            from ._exceptions import DirectoryNotFoundError
            raise DirectoryNotFoundError(target_dir)

    # List and match files
    filenames = ListFiles(source_dir)

    # Check if we have a source directory
    if filenames is None:
        return

    # Copy files
    for i_filename in filenames:
        if md5_check and i_filename.endswith('.md5'):
            continue  # md5 files will be copied by CopyFile when copying their associated files

        if fnmatch.fnmatch(i_filename, source_mask):
            source_path = source_dir + '/' + i_filename
            target_path = target_dir + '/' + i_filename

            if IsDir(source_path):
                # If we found a directory, copy it recursively
                CopyFiles(source_path, target_path, create_target_dir=True, md5_check=md5_check)
            else:
                CopyFile(source_path, target_path, md5_check=md5_check)