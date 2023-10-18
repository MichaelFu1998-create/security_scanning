def _tmdd_datetime_to_iso(dt, include_offset=True, include_seconds=True):
    """
    dt is an xml Element with <date>, <time>, and optionally <offset> children.
    returns an ISO8601 string
    """
    datestring = dt.findtext('date')
    timestring = dt.findtext('time')
    assert len(datestring) == 8
    assert len(timestring) >= 6
    iso = datestring[0:4] + '-' + datestring[4:6] + '-' + datestring[6:8] + 'T' \
        + timestring[0:2] + ':' + timestring[2:4]
    if include_seconds:
        iso += ':' + timestring[4:6]
    if include_offset:
        offset = dt.findtext('offset')
        if offset:
            assert len(offset) == 5
            iso += offset[0:3] + ':' + offset[3:5]
        else:
            raise Exception("TMDD date is not timezone-aware: %s" % etree.tostring(dt))
    return iso