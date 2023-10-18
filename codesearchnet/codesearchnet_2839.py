def get_component_tasks(self, component_id):
    """Returns the task ids allocated for the given component id"""
    ret = []
    for task_id, comp_id in self.task_to_component_map.items():
      if comp_id == component_id:
        ret.append(task_id)
    return ret