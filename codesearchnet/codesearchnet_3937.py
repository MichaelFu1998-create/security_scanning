def _symlink(path, link, overwrite=0, verbose=0):
    """
    Windows helper for ub.symlink
    """
    if exists(link) and not os.path.islink(link):
        # On windows a broken link might still exist as a hard link or a
        # junction. Overwrite it if it is a file and we cannot symlink.
        # However, if it is a non-junction directory then do not overwrite
        if verbose:
            print('link location already exists')
        is_junc = _win32_is_junction(link)
        # NOTE:
        # in python2 broken junctions are directories and exist
        # in python3 broken junctions are directories and do not exist
        if os.path.isdir(link):
            if is_junc:
                pointed = _win32_read_junction(link)
                if path == pointed:
                    if verbose:
                        print('...and is a junction that points to the same place')
                    return link
                else:
                    if verbose:
                        if not exists(pointed):
                            print('...and is a broken junction that points somewhere else')
                        else:
                            print('...and is a junction that points somewhere else')
            else:
                if verbose:
                    print('...and is an existing real directory!')
                raise IOError('Cannot overwrite a real directory')

        elif os.path.isfile(link):
            if _win32_is_hardlinked(link, path):
                if verbose:
                    print('...and is a hard link that points to the same place')
                return link
            else:
                if verbose:
                    print('...and is a hard link that points somewhere else')
                if _win32_can_symlink():
                    raise IOError('Cannot overwrite potentially real file if we can symlink')
        if overwrite:
            if verbose:
                print('...overwriting')
            util_io.delete(link, verbose > 1)
        else:
            if exists(link):
                raise IOError('Link already exists')

    _win32_symlink2(path, link, verbose=verbose)