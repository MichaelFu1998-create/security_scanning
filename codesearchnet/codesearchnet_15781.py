def parse_report_section(config_obj, section):
  """
  parse the [REPORT] section of a config file to extract various reporting options to be passed to the Report object
  :param: config_obj : configparser object for the config file passed in to naarad
  :param: section: name of the section. 'REPORT' should be passed in here
  :return: report_kwargs: dictionary of Reporting options and values specified in config.
  """
  report_kwargs = {}
  if config_obj.has_option(section, 'stylesheet_includes'):
    report_kwargs['stylesheet_includes'] = config_obj.get(section, 'stylesheet_includes')
  if config_obj.has_option(section, 'javascript_includes'):
    report_kwargs['javascript_includes'] = config_obj.get(section, 'javascript_includes')
  if config_obj.has_option(section, 'header_template'):
    report_kwargs['header_template'] = config_obj.get(section, 'header_template')
  if config_obj.has_option(section, 'footer_template'):
    report_kwargs['footer_template'] = config_obj.get(section, 'footer_template')
  if config_obj.has_option(section, 'summary_content_template'):
    report_kwargs['summary_content_template'] = config_obj.get(section, 'summary_content_template')
  if config_obj.has_option(section, 'summary_page_template'):
    report_kwargs['summary_page_template'] = config_obj.get(section, 'summary_page_template')
  if config_obj.has_option(section, 'metric_page_template'):
    report_kwargs['metric_page_template'] = config_obj.get(section, 'metric_page_template')
  if config_obj.has_option(section, 'client_charting_template'):
    report_kwargs['client_charting_template'] = config_obj.get(section, 'client_charting_template')
  if config_obj.has_option(section, 'diff_client_charting_template'):
    report_kwargs['diff_client_charting_template'] = config_obj.get(section, 'diff_client_charting_template')
  if config_obj.has_option(section, 'diff_page_template'):
    report_kwargs['diff_page_template'] = config_obj.get(section, 'diff_page_template')
  return report_kwargs