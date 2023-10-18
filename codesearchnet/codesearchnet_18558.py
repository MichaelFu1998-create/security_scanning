def fileobj(prev, file_handle, endl='', thru=False):
    """This pipe read/write data from/to file object which specified by
    file_handle.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param file_handle: The file object to read or write.
    :type file_handle: file object
    :param endl: The end-of-line symbol for each output.
    :type endl: str
    :param thru: If true, data will passed to next generator. If false, data
                 will be dropped.
    :type thru: bool
    :returns: generator
    """
    if prev is not None:
        for i in prev:
            file_handle.write(str(i)+endl)
            if thru:
                yield i
    else:
        for data in file_handle:
            yield data