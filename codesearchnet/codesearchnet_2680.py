def _start_processes(self, commands):
    """Start all commands and add them to the dict of processes to be monitored """
    Log.info("Start processes")
    processes_to_monitor = {}
    # First start all the processes
    for (name, command) in commands.items():
      p = self._run_process(name, command)
      processes_to_monitor[p.pid] = ProcessInfo(p, name, command)

      # Log down the pid file
      log_pid_for_process(name, p.pid)

    with self.process_lock:
      self.processes_to_monitor.update(processes_to_monitor)