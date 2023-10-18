def match_list(lst, pattern, group_names=[]):
    """
    Parameters
    ----------
    lst: list of str

    regex: string

    group_names: list of strings
        See re.MatchObject group docstring

    Returns
    -------
    list of strings
        Filtered list, with the strings that match the pattern
    """
    filtfn = re.compile(pattern).match
    filtlst = filter_list(lst, filtfn)
    if not group_names:
        return [m.string for m in filtlst]
    else:
        return [m.group(group_names) for m in filtlst]