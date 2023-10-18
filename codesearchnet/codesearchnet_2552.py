def start(self):
    """ state Zookeeper """
    if self.is_host_port_reachable():
      self.client = self._kazoo_client(_makehostportlist(self.hostportlist))
    else:
      localhostports = self.establish_ssh_tunnel()
      self.client = self._kazoo_client(_makehostportlist(localhostports))
    self.client.start()

    def on_connection_change(state):
      """ callback to log """
      LOG.info("Connection state changed to: " + state)
    self.client.add_listener(on_connection_change)