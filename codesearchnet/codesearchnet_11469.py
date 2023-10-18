def matches_masks(target, masks):
    """
    Determines whether or not the target string matches any of the regular
    expressions specified.

    :param target: the string to check
    :type target: str
    :param masks: the regular expressions to check against
    :type masks: list(regular expression object)
    :returns: bool
    """

    for mask in masks:
        if mask.search(target):
            return True
    return False