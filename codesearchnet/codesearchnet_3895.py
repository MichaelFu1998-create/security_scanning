def _proc_iteroutput_select(proc):
    """
    Iterates over output from a process line by line

    UNIX only. Use `_proc_iteroutput_thread` instead for a cross platform
    solution based on threads.

    Yields:
        Tuple[str, str]: oline, eline: stdout and stderr line
    """
    from six.moves import zip_longest
    # Read output while the external program is running
    while proc.poll() is None:
        reads = [proc.stdout.fileno(), proc.stderr.fileno()]
        ret = select.select(reads, [], [])
        oline = eline = None
        for fd in ret[0]:
            if fd == proc.stdout.fileno():
                oline = proc.stdout.readline()
            if fd == proc.stderr.fileno():
                eline = proc.stderr.readline()
        yield oline, eline

    # Grab any remaining data in stdout and stderr after the process finishes
    oline_iter = _textio_iterlines(proc.stdout)
    eline_iter = _textio_iterlines(proc.stderr)
    for oline, eline in zip_longest(oline_iter, eline_iter):
        yield oline, eline