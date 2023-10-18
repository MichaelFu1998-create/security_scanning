def get_git_version(git_path=None):
    """
    Get the Git version.
    """
    if git_path is None: git_path = GIT_PATH
    git_version = check_output([git_path, "--version"]).split()[2]
    return git_version