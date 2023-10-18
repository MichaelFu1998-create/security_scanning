def _map_timezones():
    """
    Map the official Haystack timezone list to those recognised by pytz.
    """
    tz_map = {}
    todo = HAYSTACK_TIMEZONES_SET.copy()
    for full_tz in pytz.all_timezones:
        # Finished case:
        if not bool(todo): # pragma: no cover
            # This is nearly impossible for us to cover, and an unlikely case.
            break

        # Case 1: exact match
        if full_tz in todo:
            tz_map[full_tz] = full_tz   # Exact match
            todo.discard(full_tz)
            continue

        # Case 2: suffix match after '/'
        if '/' not in full_tz:
            continue

        (prefix, suffix) = full_tz.split('/',1)
        # Case 2 exception: full timezone contains more than one '/' -> ignore
        if '/' in suffix:
            continue

        if suffix in todo:
            tz_map[suffix] = full_tz
            todo.discard(suffix)
            continue

    return tz_map