def set_physical_plan(self, physical_plan):
    """ set physical plan """
    if not physical_plan:
      self.physical_plan = None
      self.id = None
    else:
      self.physical_plan = physical_plan
      self.id = physical_plan.topology.id
    self.trigger_watches()