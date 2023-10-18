def walk(prev, inital_path, *args, **kw):
    """This pipe wrap os.walk and yield absolute path one by one.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param args: The end-of-line symbol for each output.
    :type args: list of string.
    :param kw: The end-of-line symbol for each output.
    :type kw: dictionary of options. Add 'endl' in kw to specify end-of-line symbol.
    :returns: generator
    """
    for dir_path, dir_names, filenames in os.walk(inital_path):
        for filename in filenames:
            yield os.path.join(dir_path, filename)