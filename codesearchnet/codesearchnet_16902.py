def timezone(haystack_tz, version=LATEST_VER):
    """
    Retrieve the Haystack timezone
    """
    tz_map = get_tz_map(version=version)
    try:
        tz_name = tz_map[haystack_tz]
    except KeyError:
        raise ValueError('%s is not a recognised timezone on this host' \
                % haystack_tz)
    return pytz.timezone(tz_name)