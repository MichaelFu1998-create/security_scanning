def try_read_file(s):
    """ If `s` is a file name, read the file and return it's content.
        Otherwise, return the original string.
        Returns None if the file was opened, but errored during reading.
    """
    try:
        with open(s, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        # Not a file name.
        return s
    except EnvironmentError as ex:
        print_err('\nFailed to read file: {}\n  {}'.format(s, ex))
        return None
    return data