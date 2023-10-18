def set_packing_plan(self, packing_plan):
    """ set packing plan """
    if not packing_plan:
      self.packing_plan = None
      self.id = None
    else:
      self.packing_plan = packing_plan
      self.id = packing_plan.id
    self.trigger_watches()