def run(self, analysis, is_api_call, **kwargs):
    """
    :param analysis: Run naarad analysis for the specified analysis object
    :param **kwargs: Additional keyword args can be passed in here for future enhancements
    :return:
    """
    threads = []
    crossplots = []
    report_args = {}
    metrics = defaultdict()
    run_steps = defaultdict(list)
    discovery_mode = False
    graph_timezone = None
    graphing_library = None

    if isinstance(analysis.config, str):
      if not naarad.utils.is_valid_file(analysis.config):
        return CONSTANTS.INVALID_CONFIG
      config_object = ConfigParser.ConfigParser(analysis.variables)
      config_object.optionxform = str
      config_object.read(analysis.config)
    elif isinstance(analysis.config, ConfigParser.ConfigParser):
      config_object = analysis.config
    else:
      if is_api_call:
        return CONSTANTS.INVALID_CONFIG
      else:
        metrics['metrics'] = naarad.utils.discover_by_name(analysis.input_directory, analysis.output_directory)
        if len(metrics['metrics']) == 0:
          logger.warning('Unable to auto detect metrics in the specified input directory: %s', analysis.input_directory)
          return CONSTANTS.ERROR
        else:
          discovery_mode = True
          metrics['aggregate_metrics'] = []
    if not discovery_mode:
      metrics, run_steps, crossplots, report_args, graph_timezone, graphing_library = self._process_naarad_config(config_object, analysis)

    if graphing_library is None:
      graphing_library = CONSTANTS.DEFAULT_GRAPHING_LIBRARY
    # If graphing libraries are not installed, skip static images
    if graphing_library not in self.available_graphing_modules.keys():
      logger.error("Naarad cannot import graphing library %s on your system. Will not generate static charts", graphing_library)
      self.skip_plots = True

    if not is_api_call:
      self._run_pre(analysis, run_steps['pre'])
    for metric in metrics['metrics']:
      if analysis.ts_start:
        metric.ts_start = analysis.ts_start
      if analysis.ts_end:
        metric.ts_end = analysis.ts_end
      thread = threading.Thread(target=naarad.utils.parse_and_plot_single_metrics,
                                args=(metric, graph_timezone, analysis.output_directory, analysis.input_directory, graphing_library, self.skip_plots))
      thread.start()
      threads.append(thread)
    for t in threads:
      t.join()
    for metric in metrics['aggregate_metrics']:
      thread = threading.Thread(target=naarad.utils.parse_and_plot_single_metrics,
                                args=(metric, graph_timezone, analysis.output_directory, analysis.input_directory, graphing_library, self.skip_plots))
      thread.start()
      threads.append(thread)
    for t in threads:
      t.join()
    self._set_sla_data(analysis.test_id, metrics['metrics'] + metrics['aggregate_metrics'])
    self._set_stats_data(analysis.test_id, metrics['metrics'] + metrics['aggregate_metrics'])
    if len(crossplots) > 0 and not self.skip_plots:
      correlated_plots = naarad.utils.nway_plotting(crossplots, metrics['metrics'] + metrics['aggregate_metrics'],
                                                    os.path.join(analysis.output_directory, analysis.resource_path),
                                                    analysis.resource_path, graphing_library)
    else:
      correlated_plots = []
    rpt = reporting_modules['report'](None, analysis.output_directory, os.path.join(analysis.output_directory, analysis.resource_path), analysis.resource_path,
                                      metrics['metrics'] + metrics['aggregate_metrics'], correlated_plots=correlated_plots, **report_args)
    rpt.generate()
    if not is_api_call:
      self._run_post(run_steps['post'])

    if self.return_exit_code:
      for metric in metrics['metrics'] + metrics['aggregate_metrics']:
        if metric.status == CONSTANTS.SLA_FAILED:
          return CONSTANTS.SLA_FAILURE

    return CONSTANTS.OK