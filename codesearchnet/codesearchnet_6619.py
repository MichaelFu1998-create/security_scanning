def is_running_on_macos():
    """
    Returns a truth value for a proposition: "the program is running on a
    macOS machine".

    :rtype: bool
    """
    pattern = re.compile('darwin', re.IGNORECASE)
    return False if not pattern.search(platform.platform()) else True