def proc_ovrds(**kwargs):
    """
    Bloomberg overrides

    Args:
        **kwargs: overrides

    Returns:
        list of tuples

    Examples:
        >>> proc_ovrds(DVD_Start_Dt='20180101')
        [('DVD_Start_Dt', '20180101')]
        >>> proc_ovrds(DVD_Start_Dt='20180101', cache=True, has_date=True)
        [('DVD_Start_Dt', '20180101')]
    """
    return [
        (k, v) for k, v in kwargs.items()
        if k not in list(ELEM_KEYS.keys()) + list(ELEM_KEYS.values()) + PRSV_COLS
    ]