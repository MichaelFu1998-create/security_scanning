def get_packing_plan(self, topologyName, callback=None):
    """ get packing plan """
    if callback:
      self.packing_plan_watchers[topologyName].append(callback)
    else:
      packing_plan_path = self.get_packing_plan_path(topologyName)
      with open(packing_plan_path) as f:
        data = f.read()
        packing_plan = PackingPlan()
        packing_plan.ParseFromString(data)