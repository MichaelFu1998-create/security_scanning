def CopyFilesX(file_mapping):
    '''
    Copies files into directories, according to a file mapping

    :param list(tuple(unicode,unicode)) file_mapping:
        A list of mappings between the directory in the target and the source.
        For syntax, @see: ExtendedPathMask

    :rtype: list(tuple(unicode,unicode))
    :returns:
        List of files copied. (source_filename, target_filename)

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    # List files that match the mapping
    files = []
    for i_target_path, i_source_path_mask in file_mapping:
        tree_recurse, flat_recurse, dirname, in_filters, out_filters = ExtendedPathMask.Split(i_source_path_mask)

        _AssertIsLocal(dirname)

        filenames = FindFiles(dirname, in_filters, out_filters, tree_recurse)
        for i_source_filename in filenames:
            if os.path.isdir(i_source_filename):
                continue  # Do not copy dirs

            i_target_filename = i_source_filename[len(dirname) + 1:]
            if flat_recurse:
                i_target_filename = os.path.basename(i_target_filename)
            i_target_filename = os.path.join(i_target_path, i_target_filename)

            files.append((
                StandardizePath(i_source_filename),
                StandardizePath(i_target_filename)
            ))

    # Copy files
    for i_source_filename, i_target_filename in files:
        # Create target dir if necessary
        target_dir = os.path.dirname(i_target_filename)
        CreateDirectory(target_dir)

        CopyFile(i_source_filename, i_target_filename)

    return files