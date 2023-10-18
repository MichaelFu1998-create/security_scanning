def check_max_filesize(chosen_file, max_size):
    """
    Checks file sizes for host
    """
    if os.path.getsize(chosen_file) > max_size:
        return False
    else:
        return True