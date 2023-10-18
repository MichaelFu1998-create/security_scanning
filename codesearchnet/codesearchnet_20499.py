def filter_list(lst, pattern):
    """
    Filters the lst using pattern.
    If pattern starts with '(' it will be considered a re regular expression,
    otherwise it will use fnmatch filter.

    :param lst: list of strings

    :param pattern: string

    :return: list of strings
    Filtered list of strings
    """
    if is_fnmatch_regex(pattern) and not is_regex(pattern):
        #use fnmatch
        log.info('Using fnmatch for {0}'.format(pattern))
        filst = fnmatch.filter(lst, pattern)

    else:
        #use re
        log.info('Using regex match for {0}'.format(pattern))
        filst = match_list(lst, pattern)

    if filst:
        filst.sort()

    return filst