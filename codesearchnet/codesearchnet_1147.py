def getAllMetrics(self):
    """Retrives a dictionary of metrics that combines all report and
    optimization metrics

    Parameters:
    ----------------------------------------------------------------------
    retval:         a dictionary of optimization metrics that were collected
                    for the model; an empty dictionary if there aren't any.
    """
    result = self.getReportMetrics()
    result.update(self.getOptimizationMetrics())
    return result