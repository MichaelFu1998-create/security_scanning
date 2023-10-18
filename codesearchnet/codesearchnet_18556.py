def stdout(prev, endl='\n', thru=False):
    """This pipe read data from previous iterator and write it to stdout.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param endl: The end-of-line symbol for each output.
    :type endl: str
    :param thru: If true, data will passed to next generator. If false, data
                 will be dropped.
    :type thru: bool
    :returns: generator
    """
    for i in prev:
        sys.stdout.write(str(i) + endl)
        if thru:
            yield i