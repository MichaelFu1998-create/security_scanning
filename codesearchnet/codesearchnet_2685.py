def start_state_manager_watches(self):
    """
    Receive updates to the packing plan from the statemgrs and update processes as needed.
    """
    Log.info("Start state manager watches")
    statemgr_config = StateMgrConfig()
    statemgr_config.set_state_locations(configloader.load_state_manager_locations(
        self.cluster, state_manager_config_file=self.state_manager_config_file,
        overrides={"heron.statemgr.connection.string": self.state_manager_connection}))
    try:
      self.state_managers = statemanagerfactory.get_all_state_managers(statemgr_config)
      for state_manager in self.state_managers:
        state_manager.start()
    except Exception as ex:
      Log.error("Found exception while initializing state managers: %s. Bailing out..." % ex)
      traceback.print_exc()
      sys.exit(1)

    # pylint: disable=unused-argument
    def on_packing_plan_watch(state_manager, new_packing_plan):
      Log.debug("State watch triggered for PackingPlan update on shard %s. Existing: %s, New: %s" %
                (self.shard, str(self.packing_plan), str(new_packing_plan)))

      if self.packing_plan != new_packing_plan:
        Log.info("PackingPlan change detected on shard %s, relaunching effected processes."
                 % self.shard)
        self.update_packing_plan(new_packing_plan)

        Log.info("Updating executor processes")
        self.launch()
      else:
        Log.info(
            "State watch triggered for PackingPlan update but plan not changed so not relaunching.")

    for state_manager in self.state_managers:
      # The callback function with the bound
      # state_manager as first variable.
      onPackingPlanWatch = functools.partial(on_packing_plan_watch, state_manager)
      state_manager.get_packing_plan(self.topology_name, onPackingPlanWatch)
      Log.info("Registered state watch for packing plan changes with state manager %s." %
               str(state_manager))