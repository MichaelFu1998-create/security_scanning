def readline(prev, filename=None, mode='r', trim=str.rstrip, start=1, end=sys.maxsize):
    """This pipe get filenames or file object from previous pipe and read the
    content of file. Then, send the content of file line by line to next pipe.

    The start and end parameters are used to limit the range of reading from file.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param filename: The files to be read. If None, use previous pipe input as filenames.
    :type filename: None|str|unicode|list|tuple
    :param mode: The mode to open file. default is 'r'
    :type mode: str
    :param trim: The function to trim the line before send to next pipe.
    :type trim: function object.
    :param start: if star is specified, only line number larger or equal to start will be sent.
    :type start: integer
    :param end: The last line number to read.
    :type end: integer
    :returns: generator
    """
    if prev is None:
        if filename is None:
            raise Exception('No input available for readline.')
        elif is_str_type(filename):
            file_list = [filename, ]
        else:
            file_list = filename
    else:
        file_list = prev

    for fn in file_list:
        if isinstance(fn, file_type):
            fd = fn
        else:
            fd = open(fn, mode)

        try:
            if start <= 1 and end == sys.maxsize:
                for line in fd:
                    yield trim(line)
            else:
                for line_no, line in enumerate(fd, 1):
                    if line_no < start:
                        continue
                    yield trim(line)
                    if line_no >= end:
                        break
        finally:
            if fd != fn:
                fd.close()