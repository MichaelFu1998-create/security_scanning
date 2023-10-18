def is_host_port_reachable(self):
    """
    Returns true if the host is reachable. In some cases, it may not be reachable a tunnel
    must be used.
    """
    for hostport in self.hostportlist:
      try:
        socket.create_connection(hostport, StateManager.TIMEOUT_SECONDS)
        return True
      except:
        LOG.info("StateManager %s Unable to connect to host: %s port %i"
                 % (self.name, hostport[0], hostport[1]))
        continue
    return False