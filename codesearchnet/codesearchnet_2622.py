def get_all_file_state_managers(conf):
  """
  Returns all the file state_managers.
  """
  state_managers = []
  state_locations = conf.get_state_locations_of_type("file")
  for location in state_locations:
    name = location['name']
    rootpath = os.path.expanduser(location['rootpath'])
    LOG.info("Connecting to file state with rootpath: " + rootpath)
    state_manager = FileStateManager(name, rootpath)
    state_managers.append(state_manager)

  return state_managers