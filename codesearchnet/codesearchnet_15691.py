def _ensure_datetime_to_string(maybe_dttm):
    """If maybe_dttm is a datetime instance, convert to a STIX-compliant
    string representation.  Otherwise return the value unchanged."""
    if isinstance(maybe_dttm, datetime.datetime):
        maybe_dttm = _format_datetime(maybe_dttm)
    return maybe_dttm