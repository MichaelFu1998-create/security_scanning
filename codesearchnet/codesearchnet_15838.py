def _extract_input_connections(self):
    """
    Given user input of interested connections, it will extract the info and output a list of tuples.
    - input can be multiple values, separated by space;
    - either host or port is optional
    - it may be just one end,
    - e.g., "host1<->host2 host3<->  host1:port1<->host2"
    :return: None
    """
    for con in self.connections:
      ends = con.strip().split('<->')  # [host1:port1->host2]
      ends = filter(None, ends)  # Remove '' elements
      if len(ends) == 0:
        continue
      if len(ends) > 0:
        host1, port1 = self._get_tuple(ends[0].split(':'))
      host2 = ''
      port2 = ''
      if len(ends) > 1:
        host2, port2 = self._get_tuple(ends[1].split(':'))
      self.input_connections.append((host1, port1, host2, port2))