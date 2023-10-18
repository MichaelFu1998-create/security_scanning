def num_instances(self):
    """
    Number of spouts + bolts
    """
    num = 0

    # Get all the components
    components = self.spouts() + self.bolts()

    # Get instances for each worker
    for component in components:
      config = component.comp.config
      for kvs in config.kvs:
        if kvs.key == api_constants.TOPOLOGY_COMPONENT_PARALLELISM:
          num += int(kvs.value)
          break

    return num