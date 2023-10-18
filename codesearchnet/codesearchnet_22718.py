def _CopyFileLocal(source_filename, target_filename, copy_symlink=True):
    '''
    Copy a file locally to a directory.

    :param unicode source_filename:
        The filename to copy from.

    :param unicode target_filename:
        The filename to copy to.

    :param bool copy_symlink:
        If True and source_filename is a symlink, target_filename will also be created as
        a symlink.

        If False, the file being linked will be copied instead.
    '''
    import shutil
    try:
        # >>> Create the target_filename directory if necessary
        dir_name = os.path.dirname(target_filename)
        if dir_name and not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        if copy_symlink and IsLink(source_filename):
            # >>> Delete the target_filename if it already exists
            if os.path.isfile(target_filename) or IsLink(target_filename):
                DeleteFile(target_filename)

            # >>> Obtain the relative path from link to source_filename (linkto)
            source_filename = ReadLink(source_filename)
            CreateLink(source_filename, target_filename)
        else:
            # shutil can't copy links in Windows, so we must find the real file manually
            if sys.platform == 'win32':
                while IsLink(source_filename):
                    link = ReadLink(source_filename)
                    if os.path.isabs(link):
                        source_filename = link
                    else:
                        source_filename = os.path.join(os.path.dirname(source_filename), link)

            shutil.copyfile(source_filename, target_filename)
            shutil.copymode(source_filename, target_filename)
    except Exception as e:
        reraise(e, 'While executiong _filesystem._CopyFileLocal(%s, %s)' % (source_filename, target_filename))