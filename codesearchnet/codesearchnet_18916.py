def __get_rev(self, key, version, **kwa):
    '''Obtain particular version of the doc at key.'''
    if '_doc' in kwa:
      doc = kwa['_doc']
    else:
      if type(version) is int:
        if version == 0:
          order = pymongo.ASCENDING
        elif version == -1:
          order = pymongo.DESCENDING
        doc = self._collection.find_one({'k': key}, sort=[['d', order]])
      elif type(version) is datetime:
        ver = self.__round_time(version)
        doc = self._collection.find_one({'k': key, 'd': ver})

    if doc is None:
      raise KeyError('Supplied key `{0}` or version `{1}` does not exist'
          .format(key, str(version)))

    coded_val = doc['v']
    return pickle.loads(coded_val)