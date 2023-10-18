def analyze(self, input_directory, output_directory, **kwargs):
    """
    Run all the analysis saved in self._analyses, sorted by test_id.
    This is useful when Naarad() is used by other programs and multiple analyses are run
    In naarad CLI mode, len(_analyses) == 1
    :param: input_directory: location of log files
    :param: output_directory: root directory for analysis output
    :param: **kwargs: Optional keyword args
    :return: int: status code.
    """
    is_api_call = True
    if len(self._analyses) == 0:
      if 'config' not in kwargs.keys():
        return CONSTANTS.ERROR
      self.create_analysis(kwargs['config'])
    if 'args' in kwargs:
      self._process_args(self._analyses[0], kwargs['args'])
      is_api_call = False
    error_count = 0
    self._input_directory = input_directory
    self._output_directory = output_directory
    for test_id in sorted(self._analyses.keys()):
      # Setup
      if not self._analyses[test_id].input_directory:
        self._analyses[test_id].input_directory = input_directory
      if not self._analyses[test_id].output_directory:
        if len(self._analyses) > 1:
          self._analyses[test_id].output_directory = os.path.join(output_directory, str(test_id))
        else:
          self._analyses[test_id].output_directory = output_directory
      if('config' in kwargs.keys()) and (not self._analyses[test_id].config):
        self._analyses[test_id].config = kwargs['config']
      self._create_output_directories(self._analyses[test_id])
      # Actually run analysis
      self._analyses[test_id].status = self.run(self._analyses[test_id], is_api_call, **kwargs)
      if self._analyses[test_id].status != CONSTANTS.OK:
        error_count += 1
    if len(self._analyses) == 1:
      return self._analyses[0].status
    elif error_count > 0:
      return CONSTANTS.ERROR
    else:
      return CONSTANTS.OK