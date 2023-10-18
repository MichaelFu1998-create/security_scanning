def addHook(self, name, callable):
    '''
    Subscribes `callable` to listen to events of `name` type. The
    parameters passed to `callable` are dependent on the specific
    event being triggered.
    '''
    if name not in self._hooks:
      self._hooks[name] = []
    self._hooks[name].append(callable)