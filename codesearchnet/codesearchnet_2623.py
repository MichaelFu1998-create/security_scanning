def incr(self, key, to_add=1):
    """Increments the value of a given key by ``to_add``"""
    if key not in self.value:
      self.value[key] = CountMetric()
    self.value[key].incr(to_add)