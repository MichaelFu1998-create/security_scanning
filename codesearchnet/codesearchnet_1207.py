def setFieldStats(self, fieldName, fieldStats):
    """
    TODO: document
    """
    #If the stats are not fully formed, ignore.
    if fieldStats[fieldName]['min'] == None or \
      fieldStats[fieldName]['max'] == None:
        return
    self.minval = fieldStats[fieldName]['min']
    self.maxval = fieldStats[fieldName]['max']
    if self.minval == self.maxval:
      self.maxval+=1
    self._setEncoderParams()