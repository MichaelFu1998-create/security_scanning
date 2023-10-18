def _in_git_repo():
    """Returns True if inside a git repo, False otherwise"""
    ret = temple.utils.shell('git rev-parse', stderr=subprocess.DEVNULL, check=False)
    return ret.returncode == 0