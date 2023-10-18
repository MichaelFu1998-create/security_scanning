def load_file_list(path=None, regx='\.jpg', printable=True, keep_prefix=False):
    r"""Return a file list in a folder by given a path and regular expression.

    Parameters
    ----------
    path : str or None
        A folder path, if `None`, use the current directory.
    regx : str
        The regx of file name.
    printable : boolean
        Whether to print the files infomation.
    keep_prefix : boolean
        Whether to keep path in the file name.

    Examples
    ----------
    >>> file_list = tl.files.load_file_list(path=None, regx='w1pre_[0-9]+\.(npz)')

    """
    if path is None:
        path = os.getcwd()
    file_list = os.listdir(path)
    return_list = []
    for _, f in enumerate(file_list):
        if re.search(regx, f):
            return_list.append(f)
    # return_list.sort()
    if keep_prefix:
        for i, f in enumerate(return_list):
            return_list[i] = os.path.join(path, f)

    if printable:
        logging.info('Match file list = %s' % return_list)
        logging.info('Number of files = %d' % len(return_list))
    return return_list