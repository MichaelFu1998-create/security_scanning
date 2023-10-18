def get_commands_to_run(self):
    """
    Prepare either TMaster or Streaming commands according to shard.
    The Shell command is attached to all containers. The empty container plan and non-exist
    container plan are bypassed.
    """
    # During shutdown the watch might get triggered with the empty packing plan
    if len(self.packing_plan.container_plans) == 0:
      return {}
    if self._get_instance_plans(self.packing_plan, self.shard) is None and self.shard != 0:
      retval = {}
      retval['heron-shell'] = Command([
          '%s' % self.heron_shell_binary,
          '--port=%s' % self.shell_port,
          '--log_file_prefix=%s/heron-shell-%s.log' % (self.log_dir, self.shard),
          '--secret=%s' % self.topology_id], self.shell_env)
      return retval

    if self.shard == 0:
      commands = self._get_tmaster_processes()
    else:
      self._untar_if_needed()
      commands = self._get_streaming_processes()

    # Attach daemon processes
    commands.update(self._get_heron_support_processes())
    return commands