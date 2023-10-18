def generateRecords(self, records):
    """Generate multiple records. Refer to definition for generateRecord"""

    if self.verbosity>0: print 'Generating', len(records), 'records...'
    for record in records:
      self.generateRecord(record)