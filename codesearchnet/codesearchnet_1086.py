def removeAllRecords(self):
    """Deletes all the values in the dataset"""

    for field in self.fields:
      field.encodings, field.values=[], []
      field.numRecords, field.numEncodings= (0, 0)