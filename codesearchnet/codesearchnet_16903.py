def timezone_name(dt, version=LATEST_VER):
    """
    Determine an appropriate timezone for the given date/time object
    """
    tz_rmap = get_tz_rmap(version=version)
    if dt.tzinfo is None:
        raise ValueError('%r has no timezone' % dt)

    # Easy case: pytz timezone.
    try:
        tz_name = dt.tzinfo.zone
        return tz_rmap[tz_name]
    except KeyError:
        # Not in timezone map
        pass
    except AttributeError:
        # Not a pytz-compatible tzinfo
        pass

    # Hard case, try to find one that's equivalent.  Hopefully we don't get
    # many of these.  Start by getting the current timezone offset, and a
    # timezone-naïve copy of the timestamp.
    offset  = dt.utcoffset()
    dt_notz = dt.replace(tzinfo=None)

    if offset == datetime.timedelta(0):
        # UTC?
        return 'UTC'

    for olson_name, haystack_name in list(tz_rmap.items()):
        if pytz.timezone(olson_name).utcoffset(dt_notz) == offset:
            return haystack_name

    raise ValueError('Unable to get timezone of %r' % dt)