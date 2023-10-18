def get_last_commit_line(git_path=None):
    """
    Get one-line description of HEAD commit for repository in current dir.
    """
    if git_path is None: git_path = GIT_PATH
    output = check_output([git_path, "log", "--pretty=format:'%ad %h %s'",
                           "--date=short", "-n1"])
    return output.strip()[1:-1]