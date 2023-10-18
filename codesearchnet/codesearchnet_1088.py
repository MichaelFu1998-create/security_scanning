def _setTypes(self, encoderSpec):
    """Set up the dataTypes and initialize encoders"""

    if self.encoderType is None:
      if self.dataType in ['int','float']:
        self.encoderType='adaptiveScalar'
      elif self.dataType=='string':
        self.encoderType='category'
      elif self.dataType in ['date', 'datetime']:
        self.encoderType='date'

    if self.dataType is None:
      if self.encoderType in ['scalar','adaptiveScalar']:
        self.dataType='float'
      elif self.encoderType in ['category', 'enumeration']:
        self.dataType='string'
      elif self.encoderType in ['date', 'datetime']:
        self.dataType='datetime'