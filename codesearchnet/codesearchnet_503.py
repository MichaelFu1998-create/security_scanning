def google2_log_prefix(level, timestamp=None, file_and_line=None):
    """Assemble a logline prefix using the google2 format."""
    # pylint: disable=global-variable-not-assigned
    global _level_names
    # pylint: enable=global-variable-not-assigned

    # Record current time
    now = timestamp or _time.time()
    now_tuple = _time.localtime(now)
    now_microsecond = int(1e6 * (now % 1.0))

    (filename, line) = file_and_line or _GetFileAndLine()
    basename = _os.path.basename(filename)

    # Severity string
    severity = 'I'
    if level in _level_names:
        severity = _level_names[level][0]

    s = '%c%02d%02d %02d: %02d: %02d.%06d %5d %s: %d] ' % (
        severity,
        now_tuple[1],  # month
        now_tuple[2],  # day
        now_tuple[3],  # hour
        now_tuple[4],  # min
        now_tuple[5],  # sec
        now_microsecond,
        _get_thread_id(),
        basename,
        line
    )

    return s