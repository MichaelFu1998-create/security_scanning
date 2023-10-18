def _win32_rmtree(path, verbose=0):
    """
    rmtree for win32 that treats junctions like directory symlinks.
    The junction removal portion may not be safe on race conditions.

    There is a known issue that prevents shutil.rmtree from
    deleting directories with junctions.
    https://bugs.python.org/issue31226
    """

    # --- old version using the shell ---
    # def _rmjunctions(root):
    #     subdirs = []
    #     for type_or_size, name, pointed in _win32_dir(root):
    #         if type_or_size == '<DIR>':
    #             subdirs.append(name)
    #         elif type_or_size == '<JUNCTION>':
    #             # remove any junctions as we encounter them
    #             # os.unlink(join(root, name))
    #             os.rmdir(join(root, name))
    #     # recurse in all real directories
    #     for name in subdirs:
    #         _rmjunctions(join(root, name))

    def _rmjunctions(root):
        subdirs = []
        for name in os.listdir(root):
            current = join(root, name)
            if os.path.isdir(current):
                if _win32_is_junction(current):
                    # remove any junctions as we encounter them
                    os.rmdir(current)
                elif not os.path.islink(current):
                    subdirs.append(current)
        # recurse in all real directories
        for subdir in subdirs:
            _rmjunctions(subdir)

    if _win32_is_junction(path):
        if verbose:
            print('Deleting <JUNCTION> directory="{}"'.format(path))
        os.rmdir(path)
    else:
        if verbose:
            print('Deleting directory="{}"'.format(path))
        # first remove all junctions
        _rmjunctions(path)
        # now we can rmtree as normal
        import shutil
        shutil.rmtree(path)