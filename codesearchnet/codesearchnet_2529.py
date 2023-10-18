def synch_topologies(self):
    """
    Sync the topologies with the statemgrs.
    """
    self.state_managers = statemanagerfactory.get_all_state_managers(self.config.statemgr_config)
    try:
      for state_manager in self.state_managers:
        state_manager.start()
    except Exception as ex:
      Log.error("Found exception while initializing state managers: %s. Bailing out..." % ex)
      traceback.print_exc()
      sys.exit(1)

    # pylint: disable=deprecated-lambda
    def on_topologies_watch(state_manager, topologies):
      """watch topologies"""
      Log.info("State watch triggered for topologies.")
      Log.debug("Topologies: " + str(topologies))
      existingTopologies = self.getTopologiesForStateLocation(state_manager.name)
      existingTopNames = map(lambda t: t.name, existingTopologies)
      Log.debug("Existing topologies: " + str(existingTopNames))
      for name in existingTopNames:
        if name not in topologies:
          Log.info("Removing topology: %s in rootpath: %s",
                   name, state_manager.rootpath)
          self.removeTopology(name, state_manager.name)

      for name in topologies:
        if name not in existingTopNames:
          self.addNewTopology(state_manager, name)

    for state_manager in self.state_managers:
      # The callback function with the bound
      # state_manager as first variable.
      onTopologiesWatch = partial(on_topologies_watch, state_manager)
      state_manager.get_topologies(onTopologiesWatch)