def Cwd(directory):
    '''
    Context manager for current directory (uses with_statement)

    e.g.:
        # working on some directory
        with Cwd('/home/new_dir'):
            # working on new_dir

        # working on some directory again

    :param unicode directory:
        Target directory to enter
    '''
    old_directory = six.moves.getcwd()
    if directory is not None:
        os.chdir(directory)
    try:
        yield directory
    finally:
        os.chdir(old_directory)