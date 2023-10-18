def getElementsByTagName(self, name):
    '''
    DOM API: Returns all tags that match name.
    '''
    if isinstance(name, basestring):
      return self.get(name.lower())
    else:
      return None