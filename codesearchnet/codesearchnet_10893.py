def check_clean_status(git_path=None):
    """
    Returns whether there are uncommitted changes in the working dir.
    """
    output = get_status(git_path)
    is_unmodified = (len(output.strip()) == 0)
    return is_unmodified