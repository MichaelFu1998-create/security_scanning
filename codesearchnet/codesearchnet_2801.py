def get_scheduler_location(self, topologyName, callback=None):
    """
    Get scheduler location
    """
    if callback:
      self.scheduler_location_watchers[topologyName].append(callback)
    else:
      scheduler_location_path = self.get_scheduler_location_path(topologyName)
      with open(scheduler_location_path) as f:
        data = f.read()
        scheduler_location = SchedulerLocation()
        scheduler_location.ParseFromString(data)
        return scheduler_location