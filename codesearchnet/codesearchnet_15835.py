def graph(self, graphing_library='matplotlib'):
    """
    graph generates two types of graphs
    'time': generate a time-series plot for all submetrics (the x-axis is a time series)
    'cdf': generate a CDF plot for important submetrics (the x-axis shows percentiles)
    """
    logger.info('Using graphing_library {lib} for metric {name}'.format(lib=graphing_library, name=self.label))
    self.plot_cdf(graphing_library)
    self.plot_timeseries(graphing_library)
    return True