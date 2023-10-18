def getElementById(self, id):
    '''
    DOM API: Returns single element with matching id value.
    '''
    results = self.get(id=id)
    if len(results) > 1:
      raise ValueError('Multiple tags with id "%s".' % id)
    elif results:
      return results[0]
    else:
      return None