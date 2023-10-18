def diff(self, test_id_1, test_id_2, config=None, **kwargs):
    """
    Create a diff report using test_id_1 as a baseline
    :param: test_id_1: test id to be used as baseline
    :param: test_id_2: test id to compare against baseline
    :param: config file for diff (optional)
    :param: **kwargs: keyword arguments
    """
    output_directory = os.path.join(self._output_directory, 'diff_' + str(test_id_1) + '_' + str(test_id_2))
    if kwargs:
      if 'output_directory' in kwargs.keys():
        output_directory = kwargs['output_directory']
    diff_report = Diff([NaaradReport(self._analyses[test_id_1].output_directory, None),
                        NaaradReport(self._analyses[test_id_2].output_directory, None)],
                       'diff', output_directory, os.path.join(output_directory, self._resource_path),
                       self._resource_path)
    if config:
      naarad.utils.extract_diff_sla_from_config_file(diff_report, config)
    diff_report.generate()
    if diff_report.sla_failures > 0:
      return CONSTANTS.SLA_FAILURE
    if diff_report.status != 'OK':
      return CONSTANTS.ERROR
    return CONSTANTS.OK