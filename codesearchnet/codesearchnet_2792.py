def establish_ssh_tunnel(self):
    """
    Establish an ssh tunnel for each local host and port
    that can be used to communicate with the state host.
    """
    localportlist = []
    for (host, port) in self.hostportlist:
      localport = self.pick_unused_port()
      self.tunnel.append(subprocess.Popen(
          ('ssh', self.tunnelhost, '-NL127.0.0.1:%d:%s:%d' % (localport, host, port))))
      localportlist.append(('127.0.0.1', localport))
    return localportlist