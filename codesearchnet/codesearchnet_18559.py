def sh(prev, *args, **kw):
    """sh pipe execute shell command specified by args. If previous pipe exists,
    read data from it and write it to stdin of shell process. The stdout of
    shell process will be passed to next pipe object line by line.

    A optional keyword argument 'trim' can pass a function into sh pipe. It is
    used to trim the output from shell process. The default trim function is
    str.rstrip. Therefore, any space characters in tail of
    shell process output line will be removed.

    For example:

    py_files = result(sh('ls') | strip | wildcard('*.py'))

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param args: The command line arguments. It will be joined by space character.
    :type args: list of string.
    :param kw: arguments for subprocess.Popen.
    :type kw: dictionary of options.
    :returns: generator
    """
    endl = '\n' if 'endl' not in kw else kw.pop('endl')
    trim = None if 'trim' not in kw else kw.pop('trim')
    if trim is None:
        trim = bytes.rstrip if is_py3 else str.rstrip

    cmdline = ' '.join(args)
    if not cmdline:
        if prev is not None:
            for i in prev:
                yield i
        else:
            while True:
                yield None

    process = subprocess.Popen(cmdline, shell=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        **kw)
    if prev is not None:
        stdin_buffer = StringIO()
        for i in prev:
            stdin_buffer.write(i)
            if endl:
                stdin_buffer.write(endl)
        if is_py3:
            process.stdin.write(stdin_buffer.getvalue().encode('utf-8'))
        else:
            process.stdin.write(stdin_buffer.getvalue())
        process.stdin.flush()
        process.stdin.close()
        stdin_buffer.close()

    for line in process.stdout:
        yield trim(line)

    process.wait()