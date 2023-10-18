def start_process_monitor(self):
    """ Monitor all processes in processes_to_monitor dict,
    restarting any if they fail, up to max_runs times.
    """
    # Now wait for any child to die
    Log.info("Start process monitor")
    while True:
      if len(self.processes_to_monitor) > 0:
        (pid, status) = os.wait()

        with self.process_lock:
          if pid in self.processes_to_monitor.keys():
            old_process_info = self.processes_to_monitor[pid]
            name = old_process_info.name
            command = old_process_info.command
            Log.info("%s (pid=%s) exited with status %d. command=%s" % (name, pid, status, command))
            # Log the stdout & stderr of the failed process
            self._wait_process_std_out_err(name, old_process_info.process)

            # Just make it world readable
            if os.path.isfile("core.%d" % pid):
              os.system("chmod a+r core.%d" % pid)
            if old_process_info.attempts >= self.max_runs:
              Log.info("%s exited too many times" % name)
              sys.exit(1)
            time.sleep(self.interval_between_runs)
            p = self._run_process(name, command)
            del self.processes_to_monitor[pid]
            self.processes_to_monitor[p.pid] =\
              ProcessInfo(p, name, command, old_process_info.attempts + 1)

            # Log down the pid file
            log_pid_for_process(name, p.pid)