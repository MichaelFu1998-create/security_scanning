def get_failed_analyses(self):
    """
    Returns a list of test_id for which naarad analysis failed
    :return: list of test_ids
    """
    failed_analyses = []
    for test_id in self._analyses.keys():
      if self._analyses[test_id].status != CONSTANTS.OK:
        failed_analyses.append(test_id)
    return failed_analyses