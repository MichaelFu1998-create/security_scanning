def launch(self):
    ''' Determines the commands to be run and compares them with the existing running commands.
    Then starts new ones required and kills old ones no longer required.
    '''
    with self.process_lock:
      current_commands = dict(map((lambda process: (process.name, process.command)),
                                  self.processes_to_monitor.values()))
      updated_commands = self.get_commands_to_run()

      # get the commands to kill, keep and start
      commands_to_kill, commands_to_keep, commands_to_start = \
          self.get_command_changes(current_commands, updated_commands)

      Log.info("current commands: %s" % sorted(current_commands.keys()))
      Log.info("new commands    : %s" % sorted(updated_commands.keys()))
      Log.info("commands_to_kill: %s" % sorted(commands_to_kill.keys()))
      Log.info("commands_to_keep: %s" % sorted(commands_to_keep.keys()))
      Log.info("commands_to_start: %s" % sorted(commands_to_start.keys()))

      self._kill_processes(commands_to_kill)
      self._start_processes(commands_to_start)
      Log.info("Launch complete - processes killed=%s kept=%s started=%s monitored=%s" %
               (len(commands_to_kill), len(commands_to_keep),
                len(commands_to_start), len(self.processes_to_monitor)))