def getTopologiesForStateLocation(self, name):
    """
    Returns all the topologies for a given state manager.
    """
    return filter(lambda t: t.state_manager_name == name, self.topologies)