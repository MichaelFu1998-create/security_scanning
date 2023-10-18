def add_key(self, key):
    """Adds a new key to this metric"""
    if key not in self.value:
      self.value[key] = ReducedMetric(self.reducer)