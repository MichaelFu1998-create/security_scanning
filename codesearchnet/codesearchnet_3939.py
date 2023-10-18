def _win32_symlink(path, link, verbose=0):
    """
    Creates real symlink. This will only work in versions greater than Windows
    Vista. Creating real symlinks requires admin permissions or at least
    specially enabled symlink permissions. On Windows 10 enabling developer
    mode should give you these permissions.
    """
    from ubelt import util_cmd
    if os.path.isdir(path):
        # directory symbolic link
        if verbose:
            print('... as directory symlink')
        command = 'mklink /D "{}" "{}"'.format(link, path)
        # Using the win32 API seems to result in privilege errors
        # but using shell commands does not have this problem. Weird.
        # jwfs.symlink(path, link, target_is_directory=True)
        # TODO: what do we need to do to use the windows api instead of shell?
    else:
        # file symbolic link
        if verbose:
            print('... as file symlink')
        command = 'mklink "{}" "{}"'.format(link, path)

    if command is not None:
        info = util_cmd.cmd(command, shell=True)
        if info['ret'] != 0:
            from ubelt import util_format
            permission_msg = 'You do not have sufficient privledges'
            if permission_msg not in info['err']:
                print('Failed command:')
                print(info['command'])
                print(util_format.repr2(info, nl=1))
            raise OSError(str(info))
    return link