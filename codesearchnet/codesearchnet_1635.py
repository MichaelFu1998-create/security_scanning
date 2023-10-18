def mmGetMetricFromTrace(self, trace):
    """
    Convenience method to compute a metric over an indices trace, excluding
    resets.

    @param (IndicesTrace) Trace of indices

    @return (Metric) Metric over trace excluding resets
    """
    return Metric.createFromTrace(trace.makeCountsTrace(),
                                  excludeResets=self.mmGetTraceResets())