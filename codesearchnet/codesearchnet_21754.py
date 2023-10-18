def _iter_filepaths_with_extension(extname, root_dir='.'):
    """Iterative over relative filepaths of files in a directory, and
    sub-directories, with the given extension.

    Parameters
    ----------
    extname : `str`
        Extension name (such as 'txt' or 'rst'). Extension comparison is
        case sensitive.
    root_dir : 'str`, optional
        Root directory. Current working directory by default.

    Yields
    ------
    filepath : `str`
        File path, relative to ``root_dir``, with the given extension.
    """
    # needed for comparison with os.path.splitext
    if not extname.startswith('.'):
        extname = '.' + extname

    root_dir = os.path.abspath(root_dir)

    for dirname, sub_dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if os.path.splitext(filename)[-1] == extname:
                full_filename = os.path.join(dirname, filename)
                rel_filepath = os.path.relpath(full_filename, start=root_dir)
                yield rel_filepath