def print_summary(string='Repository', git_path=None):
    """
    Print the last commit line and eventual uncommitted changes.
    """
    if git_path is None: git_path = GIT_PATH

    # If git is available, check fretbursts version
    if not git_path_valid():
        print('\n%s revision unknown (git not found).' % string)
    else:
        last_commit = get_last_commit_line()
        print('\n{} revision:\n {}\n'.format(string, last_commit))
        if not check_clean_status():
            print('\nWARNING -> Uncommitted changes:')
            print(get_status())