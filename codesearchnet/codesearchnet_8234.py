def pid_context(pid_filename=None):
    """
    For the duration of this context manager, put the PID for this process into
    `pid_filename`, and then remove the file at the end.
    """
    pid_filename = pid_filename or DEFAULT_PID_FILENAME
    if os.path.exists(pid_filename):
        contents = open(pid_filename).read(16)
        log.warning('pid_filename %s already exists with contents %s',
                    pid_filename, contents)

    with open(pid_filename, 'w') as fp:
        fp.write(str(os.getpid()))
        fp.write('\n')

    try:
        yield
    finally:
        try:
            os.remove(pid_filename)
        except Exception as e:
            log.error('Got an exception %s deleting the pid_filename %s',
                      e, pid_filename)