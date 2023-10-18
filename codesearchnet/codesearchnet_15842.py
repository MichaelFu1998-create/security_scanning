def _check_connection(self, local_end, remote_end, process):
    """
    Check whether the connection is of interest or not
    :param local_end: Local connection end point, e.g., 'host1:port1'
    :param remote_end: Remote connection end point, e.g., 'host2:port2'
    :param process: Current connection 's process info, e.g., '1234/firefox'
    :return: a tuple of (local_end, remote_end, True/False); e.g. ('host1_23232', 'host2_2222', True)
    """
    # check tcp end points
    cur_host1, cur_port1 = self._get_tuple(local_end.split(':'))
    cur_host2, cur_port2 = self._get_tuple(remote_end.split(':'))

    # check whether the connection is interested or not by checking user input
    host_port_is_interested = False
    for (host1, port1, host2, port2) in self.input_connections:
      if self._match_host_port(host1, port1, cur_host1, cur_port1) and self._match_host_port(host2, port2, cur_host2, cur_port2):
        host_port_is_interested = True
        break
      if self._match_host_port(host1, port1, cur_host2, cur_port2) and self._match_host_port(host2, port2, cur_host1, cur_port1):
        host_port_is_interested = True
        break

    # check whether the connection is interested or not by checking process names given in the config
    process_is_interested = False
    for pid, name in self.input_processes:
      if self._match_processes(pid, name, process):
        process_is_interested = True
        break

    return cur_host1 + '_' + cur_port1, cur_host2 + '_' + cur_port2, host_port_is_interested and process_is_interested