def dir_maker(path):
    """Create a directory if it does not exist."""
    directory = os.path.dirname(path)
    if directory != '' and not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            sys.exit('Failed to create directory: {}'.format(e))