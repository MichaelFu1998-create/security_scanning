def getDescription(self):
    """Returns a description of the dataset"""

    description = {'name':self.name, 'fields':[f.name for f in self.fields], \
      'numRecords by field':[f.numRecords for f in self.fields]}

    return description