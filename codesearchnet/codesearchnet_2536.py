def extract_tmaster(self, topology):
    """
    Returns the representation of tmaster that will
    be returned from Tracker.
    """
    tmasterLocation = {
        "name": None,
        "id": None,
        "host": None,
        "controller_port": None,
        "master_port": None,
        "stats_port": None,
    }
    if topology.tmaster:
      tmasterLocation["name"] = topology.tmaster.topology_name
      tmasterLocation["id"] = topology.tmaster.topology_id
      tmasterLocation["host"] = topology.tmaster.host
      tmasterLocation["controller_port"] = topology.tmaster.controller_port
      tmasterLocation["master_port"] = topology.tmaster.master_port
      tmasterLocation["stats_port"] = topology.tmaster.stats_port

    return tmasterLocation