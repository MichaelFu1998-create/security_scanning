def save_traceback(err):
    """Save error traceback to bootstrapper log file.

    :param err: Catched exception.
    """
    # Store logs to ~/.bootstrapper directory
    dirname = safe_path(os.path.expanduser(
        os.path.join('~', '.{0}'.format(__script__))
    ))

    # But ensure that directory exists
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    # Now we ready to put traceback to log file
    filename = os.path.join(dirname, '{0}.log'.format(__script__))

    with open(filename, 'a+') as handler:
        traceback.print_exc(file=handler)

    # And show colorized message
    message = ('User aborted workflow'
               if isinstance(err, KeyboardInterrupt)
               else 'Unexpected error catched')
    print_error(message)
    print_error('Full log stored to {0}'.format(filename), False)

    return True