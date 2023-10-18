def get_pplan(self, topologyName, callback=None):
    """
    Get physical plan of a topology
    """
    if callback:
      self.pplan_watchers[topologyName].append(callback)
    else:
      pplan_path = self.get_pplan_path(topologyName)
      with open(pplan_path) as f:
        data = f.read()
        pplan = PhysicalPlan()
        pplan.ParseFromString(data)
        return pplan