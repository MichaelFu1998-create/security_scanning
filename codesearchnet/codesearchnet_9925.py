def already_downloaded(filename):
    """
        Verify that the file has not already been downloaded.
    """
    cur_file = os.path.join(c.bview_dir, filename)
    old_file = os.path.join(c.bview_dir, 'old', filename)
    if not os.path.exists(cur_file) and not os.path.exists(old_file):
        return False
    return True