def _find_allowed_shift(self, timestamps):
    """
    Find the maximum allowed shift steps based on max_shift_milliseconds.
    param list timestamps: timestamps of a time series.
    """
    init_ts = timestamps[0]
    residual_timestamps = map(lambda ts: ts - init_ts, timestamps)
    n = len(residual_timestamps)
    return self._find_first_bigger(residual_timestamps, self.max_shift_milliseconds, 0, n)