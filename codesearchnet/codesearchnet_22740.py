def CreateLink(target_path, link_path, override=True):
    '''
    Create a symbolic link at `link_path` pointing to `target_path`.

    :param unicode target_path:
        Link target

    :param unicode link_path:
        Fullpath to link name

    :param bool override:
        If True and `link_path` already exists as a link, that link is overridden.
    '''
    _AssertIsLocal(target_path)
    _AssertIsLocal(link_path)

    if override and IsLink(link_path):
        DeleteLink(link_path)

    # Create directories leading up to link
    dirname = os.path.dirname(link_path)
    if dirname:
        CreateDirectory(dirname)

    if sys.platform != 'win32':
        return os.symlink(target_path, link_path)  # @UndefinedVariable
    else:
        #import ntfsutils.junction
        #return ntfsutils.junction.create(target_path, link_path)

        import jaraco.windows.filesystem
        return jaraco.windows.filesystem.symlink(target_path, link_path)

        from ._easyfs_win32 import CreateSymbolicLink
        try:
            dw_flags = 0
            if target_path and os.path.isdir(target_path):
                dw_flags = 1
            return CreateSymbolicLink(target_path, link_path, dw_flags)
        except Exception as e:
            reraise(e, 'Creating link "%(link_path)s" pointing to "%(target_path)s"' % locals())