def _process_naarad_config(self, config, analysis):
    """
    Process the config file associated with a particular analysis and return metrics, run_steps and crossplots.
    Also sets output directory and resource_path for an anlaysis
    """
    graph_timezone = None
    output_directory = analysis.output_directory
    resource_path = analysis.resource_path
    run_steps = defaultdict(list)
    metrics = defaultdict(list)
    indir_default = ''
    crossplots = []
    report_args = {}
    graphing_library = None
    ts_start, ts_end = None, None

    if config.has_section('GLOBAL'):
      ts_start, ts_end = naarad.utils.parse_global_section(config, 'GLOBAL')
      if config.has_option('GLOBAL', 'user_defined_metrics'):
        naarad.utils.parse_user_defined_metric_classes(config, metric_classes)
      config.remove_section('GLOBAL')

    if config.has_section('REPORT'):
      report_args = naarad.utils.parse_report_section(config, 'REPORT')
      config.remove_section('REPORT')

    for section in config.sections():
      # GRAPH section is optional
      if section == 'GRAPH':
        graphing_library, crossplots, outdir_default, indir_default, graph_timezone = \
            naarad.utils.parse_graph_section(config, section, output_directory, indir_default)
      elif section.startswith('RUN-STEP'):
        run_step = naarad.utils.parse_run_step_section(config, section)
        if not run_step:
          logger.error('Ignoring section %s, could not parse it correctly', section)
          continue
        if run_step.run_order == CONSTANTS.PRE_ANALYSIS_RUN:
          run_steps['pre'].append(run_step)
        # DURING_ANALYSIS_RUN not supported yet
        elif run_step.run_order == CONSTANTS.DURING_ANALYSIS_RUN:
          run_steps['in'].append(run_step)
        elif run_step.run_order == CONSTANTS.POST_ANALYSIS_RUN:
          run_steps['post'].append(run_step)
        else:
          logger.error('Unknown RUN-STEP run_order specified')
      else:
        # section name is used to create sub-directories, so enforce it.
        if not naarad.utils.is_valid_metric_name(section):
          logger.critical('Section name %s is invalid! Only letters, digits, dot(.), dash(-), underscore(_) are allowed'
                          % section)
          return CONSTANTS.CRITICAL_FAILURE
        if section == 'SAR-*':
          hostname, infile, label, ts_start, ts_end, precision, kwargs, rule_strings = \
              naarad.utils.parse_basic_metric_options(config, section)
          sar_metrics = naarad.utils.get_all_sar_objects(metrics, infile, hostname, output_directory, label, ts_start,
                                                         ts_end, None)
          for sar_metric in sar_metrics:
            if sar_metric.ts_start is None and (sar_metric.ts_end is None or sar_metric.ts_end > ts_start):
              sar_metric.ts_start = ts_start
            if sar_metric.ts_end is None and (sar_metric.ts_start is None or ts_end > sar_metric.ts_start):
              sar_metric.ts_end = ts_end
          metrics['metrics'].extend(sar_metrics)
        else:
          new_metric = naarad.utils.parse_metric_section(config, section, metric_classes, metrics['metrics'],
                                                         aggregate_metric_classes, output_directory, resource_path)
          if new_metric.ts_start is None and (new_metric.ts_end is None or new_metric.ts_end > ts_start):
            new_metric.ts_start = ts_start
          if new_metric.ts_end is None and (new_metric.ts_start is None or ts_end > new_metric.ts_start):
            new_metric.ts_end = ts_end
          metric_type = section.split('-')[0]
          if metric_type in aggregate_metric_classes:
            metrics['aggregate_metrics'].append(new_metric)
          else:
            metrics['metrics'].append(new_metric)
    return metrics, run_steps, crossplots, report_args, graph_timezone, graphing_library