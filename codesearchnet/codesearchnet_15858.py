def signal_start(self, config, test_id=None, **kwargs):
    """
    Initialize an analysis object and set ts_start for the analysis represented by test_id
    :param test_id: integer that represents the analysis
    :param config: config can be a ConfigParser.ConfigParser object or a string specifying local or http(s) location
     for config
    :return: test_id
    """
    if not test_id:
      self._default_test_id += 1
      test_id = self._default_test_id
    self._analyses[test_id] = _Analysis(naarad.utils.get_standardized_timestamp('now', None), config,
                                      test_id=test_id)
    if kwargs:
      if 'description' in kwargs.keys():
        self._analyses[test_id].description = kwargs['description']
      if 'input_directory' in kwargs.keys():
        self._analyses[test_id].input_directory = kwargs['input_directory']
      if 'output_directory' in kwargs.keys():
        self._analyses[test_id].output_directory = kwargs['output_directory']
    return test_id