def _dirstats(dpath=None):  # nocover
    """
    Testing helper for printing directory information
    (mostly for investigating windows weirdness)

    CommandLine:
        python -m ubelt.util_links _dirstats
    """
    from ubelt import util_colors
    if dpath is None:
        dpath = os.getcwd()
    print('===============')
    print('Listing for dpath={}'.format(dpath))
    print('E L F D J - path')
    print('--------------')
    if not os.path.exists(dpath):
        print('... does not exist')
        return
    paths = sorted(os.listdir(dpath))
    for path in paths:
        full_path = join(dpath, path)
        E = os.path.exists(full_path)
        L = os.path.islink(full_path)
        F = os.path.isfile(full_path)
        D = os.path.isdir(full_path)
        J = util_platform.WIN32 and _win32_links._win32_is_junction(full_path)
        ELFDJ = [E, L, F, D, J]
        if   ELFDJ == [1, 0, 0, 1, 0]:
            # A directory
            path = util_colors.color_text(path, 'green')
        elif ELFDJ == [1, 0, 1, 0, 0]:
            # A file (or a hard link they are indistinguishable with one query)
            path = util_colors.color_text(path, 'white')
        elif ELFDJ == [1, 0, 0, 1, 1]:
            # A directory junction
            path = util_colors.color_text(path, 'yellow')
        elif ELFDJ == [1, 1, 1, 0, 0]:
            # A file link
            path = util_colors.color_text(path, 'turquoise')
        elif ELFDJ == [1, 1, 0, 1, 0]:
            # A directory link
            path = util_colors.color_text(path, 'teal')
        elif ELFDJ == [0, 1, 0, 0, 0]:
            # A broken file link
            path = util_colors.color_text(path, 'red')
        elif ELFDJ == [0, 1, 0, 1, 0]:
            # A broken directory link
            path = util_colors.color_text(path, 'darkred')
        elif ELFDJ == [0, 0, 0, 1, 1]:
            # A broken directory junction
            path = util_colors.color_text(path, 'purple')
        elif ELFDJ == [1, 0, 1, 0, 1]:
            # A file junction? Thats not good.
            # I guess this is a windows 7 thing?
            path = util_colors.color_text(path, 'red')
        elif ELFDJ == [1, 1, 0, 0, 0]:
            # Windows? Why? What does this mean!?
            # A directory link that cant be resolved?
            path = util_colors.color_text(path, 'red')
        else:
            print('dpath = {!r}'.format(dpath))
            print('path = {!r}'.format(path))
            raise AssertionError(str(ELFDJ) + str(path))
        line = '{E:d} {L:d} {F:d} {D:d} {J:d} - {path}'.format(**locals())
        if os.path.islink(full_path):
            line += ' -> ' + os.readlink(full_path)
        elif _win32_links is not None:
            if _win32_links._win32_is_junction(full_path):
                line += ' => ' + _win32_links._win32_read_junction(full_path)
        print(line)