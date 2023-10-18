def _get_search_path(main_file_dir, sys_path):
    '''
    Find the parent python path that contains the __main__'s file directory

    :param main_file_dir: __main__'s file directory
    :param sys_path: paths list to match directory against (like sys.path)
    '''
    # List to gather candidate parent paths
    paths = []
    # look for paths containing the directory
    for pth in sys_path:
        # convert relative path to absolute
        pth = path.abspath(pth)
        # filter out __main__'s file directory, it will be in the sys.path
        # filter in parent paths containing the package
        if (pth != main_file_dir
                and pth == path.commonprefix((pth, main_file_dir))):
            paths.append(pth)
    # check if we have results
    if paths:
        # we found candidates, look for the largest(closest) parent search path
        paths.sort()
        return paths[-1]