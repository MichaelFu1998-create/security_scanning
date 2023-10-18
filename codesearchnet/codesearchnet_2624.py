def update(self, key, value):
    """Updates a value of a given key and apply reduction"""
    if key not in self.value:
      self.value[key] = ReducedMetric(self.reducer)

    self.value[key].update(value)