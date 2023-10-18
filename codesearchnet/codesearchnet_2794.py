def monitor(self):
    """
    Monitor the rootpath and call the callback
    corresponding to the change.
    This monitoring happens periodically. This function
    is called in a seperate thread from the main thread,
    because it sleeps for the intervals between each poll.
    """

    def trigger_watches_based_on_files(watchers, path, directory, ProtoClass):
      """
      For all the topologies in the watchers, check if the data
      in directory has changed. Trigger the callback if it has.
      """
      for topology, callbacks in watchers.items():
        file_path = os.path.join(path, topology)
        data = ""
        if os.path.exists(file_path):
          with open(os.path.join(path, topology)) as f:
            data = f.read()
        if topology not in directory or data != directory[topology]:
          proto_object = ProtoClass()
          proto_object.ParseFromString(data)
          for callback in callbacks:
            callback(proto_object)
          directory[topology] = data

    while not self.monitoring_thread_stop_signal:
      topologies_path = self.get_topologies_path()

      topologies = []
      if os.path.isdir(topologies_path):
        topologies = list(filter(
            lambda f: os.path.isfile(os.path.join(topologies_path, f)),
            os.listdir(topologies_path)))
      if set(topologies) != set(self.topologies_directory):
        for callback in self.topologies_watchers:
          callback(topologies)
      self.topologies_directory = topologies

      trigger_watches_based_on_files(
          self.topology_watchers, topologies_path, self.topologies_directory, Topology)

      # Get the directory name for execution state
      execution_state_path = os.path.dirname(self.get_execution_state_path(""))
      trigger_watches_based_on_files(
          self.execution_state_watchers, execution_state_path,
          self.execution_state_directory, ExecutionState)

      # Get the directory name for packing_plan
      packing_plan_path = os.path.dirname(self.get_packing_plan_path(""))
      trigger_watches_based_on_files(
          self.packing_plan_watchers, packing_plan_path, self.packing_plan_directory, PackingPlan)

      # Get the directory name for pplan
      pplan_path = os.path.dirname(self.get_pplan_path(""))
      trigger_watches_based_on_files(
          self.pplan_watchers, pplan_path,
          self.pplan_directory, PhysicalPlan)

      # Get the directory name for tmaster
      tmaster_path = os.path.dirname(self.get_tmaster_path(""))
      trigger_watches_based_on_files(
          self.tmaster_watchers, tmaster_path,
          self.tmaster_directory, TMasterLocation)

      # Get the directory name for scheduler location
      scheduler_location_path = os.path.dirname(self.get_scheduler_location_path(""))
      trigger_watches_based_on_files(
          self.scheduler_location_watchers, scheduler_location_path,
          self.scheduler_location_directory, SchedulerLocation)

      # Sleep for some time
      self.event.wait(timeout=5)