def diff_reports_by_location(self, report1_location, report2_location, output_directory, config=None, **kwargs):
    """
    Create a diff report using report1 as a baseline
    :param: report1_location: report to be used as baseline
    :param: report2_location: report to compare against baseline
    :param: config file for diff (optional)
    :param: **kwargs: keyword arguments
    """

    if kwargs:
      if 'output_directory' in kwargs.keys():
        output_directory = kwargs['output_directory']
    diff_report = Diff([NaaradReport(report1_location, None), NaaradReport(report2_location, None)], 'diff',
                       output_directory, os.path.join(output_directory, self._resource_path), self._resource_path)
    if config:
      naarad.utils.extract_diff_sla_from_config_file(diff_report, config)
    diff_report.generate()
    if diff_report.sla_failures > 0:
      return CONSTANTS.SLA_FAILURE
    if diff_report.status != 'OK':
      return CONSTANTS.ERROR
    return CONSTANTS.OK