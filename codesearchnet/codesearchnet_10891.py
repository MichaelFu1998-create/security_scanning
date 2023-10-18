def git_path_valid(git_path=None):
    """
    Check whether the git executable is found.
    """
    if git_path is None and GIT_PATH is None:
        return False
    if git_path is None: git_path = GIT_PATH
    try:
        call([git_path, '--version'])
        return True
    except OSError:
        return False