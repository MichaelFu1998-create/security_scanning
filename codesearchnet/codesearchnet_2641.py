def build(self, bldr):
    """Builds the topology and returns the builder"""
    stage_names = sets.Set()
    for source in self._sources:
      source._build(bldr, stage_names)
    for source in self._sources:
      if not source._all_built():
        raise RuntimeError("Topology cannot be fully built! Are all sources added?")