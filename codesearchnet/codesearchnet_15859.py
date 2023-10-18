def signal_stop(self, test_id=None):
    """
    Set ts_end for the analysis represented by test_id
    :param test_id: integer that represents the analysis
    :return: test_id
    """
    if test_id is None:
      test_id = self._default_test_id
    if self._analyses[test_id].ts_end:
      return CONSTANTS.OK
    self._analyses[test_id].ts_end = naarad.utils.get_standardized_timestamp('now', None)
    return CONSTANTS.OK