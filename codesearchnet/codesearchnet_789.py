def match(self, record):
    '''
    Returns True if the record matches any of the provided filters
    '''

    for field, meta in self.filterDict.iteritems():
      index = meta['index']
      categories = meta['categories']
      for category in categories:
        # Record might be blank, handle this
        if not record:
          continue
        if record[index].find(category) != -1:
          '''
          This field contains the string we're searching for
          so we'll keep the records
          '''
          return True

    # None of the categories were found in this record
    return False