def _match_processes(self, pid, name, cur_process):
    """
    Determine whether user-specified "pid/processes" contain this process
    :param pid: The user input of pid
    :param name: The user input of process name
    :param process: current process info
    :return: True or Not; (if both pid/process are given, then both of them need to match)
    """
    cur_pid, cur_name = self._get_tuple(cur_process.split('/'))

    pid_match = False
    if not pid:
      pid_match = True
    elif pid == cur_pid:
      pid_match = True

    name_match = False
    if not name:
      name_match = True
    elif name == cur_name:
      name_match = True

    return pid_match and name_match