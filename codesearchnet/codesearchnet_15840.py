def _match_host_port(self, host, port, cur_host, cur_port):
    """
    Determine whether user-specified (host,port) matches current (cur_host, cur_port)
    :param host,port: The user input of (host,port)
    :param cur_host, cur_port: The current connection
    :return: True or Not
    """
    # if host is '', true;  if not '', it should prefix-match cur_host
    host_match = False
    if not host:
      host_match = True
    elif cur_host.startswith(host):  # allow for partial match
      host_match = True

    # if port is '', true;  if not '', it should exactly match cur_port
    port_match = False
    if not port:
      port_match = True
    elif port == cur_port:
      port_match = True

    return host_match and port_match