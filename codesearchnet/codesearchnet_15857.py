def create_analysis(self, config):
    """
    Create Analysis and save in Naarad from config
    :param config:
    :return:
    """
    self._default_test_id += 1
    self._analyses[self._default_test_id] = _Analysis(ts_start=None, config=config, test_id=self._default_test_id)