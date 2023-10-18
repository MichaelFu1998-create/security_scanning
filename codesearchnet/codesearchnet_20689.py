def dir_match(regex, wd=os.curdir):
    """Create a list of regex matches that result from the match_regex
    of all file names within wd.
    The list of files will have wd as path prefix.

    @param regex: string
    @param wd: string
    working directory
    @return:
    """
    ls = os.listdir(wd)

    filt = re.compile(regex).match
    return filter_list(ls, filt)