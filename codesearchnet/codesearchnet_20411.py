def replaced_directory(dirname):
    """This ``Context Manager`` is used to move the contents of a directory
    elsewhere temporarily and put them back upon exit.  This allows testing
    code to use the same file directories as normal code without fear of
    damage.

    The name of the temporary directory which contains your files is yielded.

    :param dirname:
        Path name of the directory to be replaced.


    Example:

    .. code-block:: python

        with replaced_directory('/foo/bar/') as rd:
            # "/foo/bar/" has been moved & renamed
            with open('/foo/bar/thing.txt', 'w') as f:
                f.write('stuff')
                f.close()


        # got here? => "/foo/bar/ is now restored and temp has been wiped, 
        # "thing.txt" is gone
    """
    if dirname[-1] == '/':
        dirname = dirname[:-1]

    full_path = os.path.abspath(dirname)
    if not os.path.isdir(full_path):
        raise AttributeError('dir_name must be a directory')

    base, name = os.path.split(full_path)

    # create a temporary directory, move provided dir into it and recreate the
    # directory for the user
    tempdir = tempfile.mkdtemp()
    shutil.move(full_path, tempdir)
    os.mkdir(full_path)
    try:
        yield tempdir

    finally:
        # done context, undo everything
        shutil.rmtree(full_path)
        moved = os.path.join(tempdir, name)
        shutil.move(moved, base)
        shutil.rmtree(tempdir)