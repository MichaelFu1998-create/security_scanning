def _ensure_managed_repos_dir_exists():
    """
    Our exports file will be invalid if this folder doesn't exist, and the NFS server
    will not run correctly.
    """
    if not os.path.exists(constants.REPOS_DIR):
        os.makedirs(constants.REPOS_DIR)