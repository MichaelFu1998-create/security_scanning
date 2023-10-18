def delete(path, verbose=False):
    """
    Removes a file or recursively removes a directory.
    If a path does not exist, then this is does nothing.

    Args:
        path (PathLike): file or directory to remove
        verbose (bool): if True prints what is being done

    SeeAlso:
        send2trash - A cross-platform Python package for sending files
            to the trash instead of irreversibly deleting them.
            https://github.com/hsoft/send2trash

    Doctest:
        >>> import ubelt as ub
        >>> base = ub.ensure_app_cache_dir('ubelt', 'delete_test')
        >>> dpath1 = ub.ensuredir(join(base, 'dir'))
        >>> ub.ensuredir(join(base, 'dir', 'subdir'))
        >>> ub.touch(join(base, 'dir', 'to_remove1.txt'))
        >>> fpath1 = join(base, 'dir', 'subdir', 'to_remove3.txt')
        >>> fpath2 = join(base, 'dir', 'subdir', 'to_remove2.txt')
        >>> ub.touch(fpath1)
        >>> ub.touch(fpath2)
        >>> assert all(map(exists, (dpath1, fpath1, fpath2)))
        >>> ub.delete(fpath1)
        >>> assert all(map(exists, (dpath1, fpath2)))
        >>> assert not exists(fpath1)
        >>> ub.delete(dpath1)
        >>> assert not any(map(exists, (dpath1, fpath1, fpath2)))

    Doctest:
        >>> import ubelt as ub
        >>> dpath = ub.ensure_app_cache_dir('ubelt', 'delete_test2')
        >>> dpath1 = ub.ensuredir(join(dpath, 'dir'))
        >>> fpath1 = ub.touch(join(dpath1, 'to_remove.txt'))
        >>> assert exists(fpath1)
        >>> ub.delete(dpath)
        >>> assert not exists(fpath1)
    """
    if not os.path.exists(path):
        # if the file does exists and is not a broken link
        if os.path.islink(path):
            if verbose:  # nocover
                print('Deleting broken link="{}"'.format(path))
            os.unlink(path)
        elif os.path.isdir(path):  # nocover
            # Only on windows will a file be a directory and not exist
            if verbose:
                print('Deleting broken directory link="{}"'.format(path))
            os.rmdir(path)
        elif os.path.isfile(path):  # nocover
            # This is a windows only case
            if verbose:
                print('Deleting broken file link="{}"'.format(path))
            os.unlink(path)
        else:
            if verbose:  # nocover
                print('Not deleting non-existant path="{}"'.format(path))
    else:
        if os.path.islink(path):
            if verbose:  # nocover
                print('Deleting symbolic link="{}"'.format(path))
            os.unlink(path)
        elif os.path.isfile(path):
            if verbose:  # nocover
                print('Deleting file="{}"'.format(path))
            os.unlink(path)
        elif os.path.isdir(path):
            if verbose:  # nocover
                print('Deleting directory="{}"'.format(path))
            if sys.platform.startswith('win32'):  # nocover
                # Workaround bug that prevents shutil from working if
                # the directory contains junctions
                from ubelt import _win32_links
                _win32_links._win32_rmtree(path, verbose=verbose)
            else:
                import shutil
                shutil.rmtree(path)