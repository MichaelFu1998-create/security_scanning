def _rectify_countdown_or_bool(count_or_bool):
    """
    used by recursive functions to specify which level to turn a bool on in
    counting down yields True, True, ..., False
    counting up yields False, False, False, ... True

    Args:
        count_or_bool (bool or int): if positive and an integer, it will count
            down, otherwise it will remain the same.

    Returns:
        int or bool: count_or_bool_

    CommandLine:
        python -m utool.util_str --test-_rectify_countdown_or_bool

    Example:
        >>> from ubelt.util_format import _rectify_countdown_or_bool  # NOQA
        >>> count_or_bool = True
        >>> a1 = (_rectify_countdown_or_bool(2))
        >>> a2 = (_rectify_countdown_or_bool(1))
        >>> a3 = (_rectify_countdown_or_bool(0))
        >>> a4 = (_rectify_countdown_or_bool(-1))
        >>> a5 = (_rectify_countdown_or_bool(-2))
        >>> a6 = (_rectify_countdown_or_bool(True))
        >>> a7 = (_rectify_countdown_or_bool(False))
        >>> a8 = (_rectify_countdown_or_bool(None))
        >>> result = [a1, a2, a3, a4, a5, a6, a7, a8]
        >>> print(result)
        [1, 0, 0, -1, -2, True, False, False]
    """
    if count_or_bool is True or count_or_bool is False:
        count_or_bool_ = count_or_bool
    elif isinstance(count_or_bool, int):
        if count_or_bool == 0:
            return 0
        elif count_or_bool > 0:
            count_or_bool_ = count_or_bool - 1
        else:
            # We dont countup negatives anymore
            count_or_bool_ = count_or_bool
    else:
        count_or_bool_ = False
    return count_or_bool_