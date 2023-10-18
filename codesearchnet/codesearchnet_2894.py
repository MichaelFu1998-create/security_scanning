def choose_tasks(self, stream_id, values):
    """Choose tasks for a given stream_id and values and Returns a list of target tasks"""
    if stream_id not in self.targets:
      return []

    ret = []
    for target in self.targets[stream_id]:
      ret.extend(target.choose_tasks(values))
    return ret