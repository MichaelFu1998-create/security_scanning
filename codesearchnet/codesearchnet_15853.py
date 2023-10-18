def _set_scores(self):
    """
    Compute anomaly scores for the time series.
    """
    anom_scores = {}
    self._compute_derivatives()
    derivatives_ema = utils.compute_ema(self.smoothing_factor, self.derivatives)
    for i, (timestamp, value) in enumerate(self.time_series_items):
      anom_scores[timestamp] = abs(self.derivatives[i] - derivatives_ema[i])
    stdev = numpy.std(anom_scores.values())
    if stdev:
        for timestamp in anom_scores.keys():
          anom_scores[timestamp] /= stdev
    self.anom_scores = TimeSeries(self._denoise_scores(anom_scores))