def _getFieldStats(self):
    """
    Method which returns a dictionary of field statistics received from the
    input source.

    Returns:

      fieldStats: dict of dicts where the first level is the field name and
        the second level is the statistic. ie. fieldStats['pounds']['min']

    """

    fieldStats = dict()
    fieldNames = self._inputSource.getFieldNames()
    for field in fieldNames:
      curStats = dict()
      curStats['min'] = self._inputSource.getFieldMin(field)
      curStats['max'] = self._inputSource.getFieldMax(field)
      fieldStats[field] = curStats
    return fieldStats