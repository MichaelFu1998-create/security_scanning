def _datetime_in_range(self, dt, dt_min=None, dt_max=None):
    """Determine if the provided time is within the range, inclusive."""
    # The pipelines API stores operation create-time with second granularity.
    # We mimic this behavior in the local provider by truncating to seconds.
    dt = dt.replace(microsecond=0)
    if dt_min:
      dt_min = dt_min.replace(microsecond=0)
    else:
      dt_min = dsub_util.replace_timezone(datetime.datetime.min, pytz.utc)
    if dt_max:
      dt_max = dt_max.replace(microsecond=0)
    else:
      dt_max = dsub_util.replace_timezone(datetime.datetime.max, pytz.utc)

    return dt_min <= dt <= dt_max