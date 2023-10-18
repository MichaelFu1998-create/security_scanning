def get_machines(self):
    """
    Get all the machines that this topology is running on.
    These are the hosts of all the stmgrs.
    """
    if self.physical_plan:
      stmgrs = list(self.physical_plan.stmgrs)
      return map(lambda s: s.host_name, stmgrs)
    return []