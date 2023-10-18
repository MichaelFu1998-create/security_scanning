def _get_heron_support_processes(self):
    """ Get a map from all daemon services' name to the command to start them """
    retval = {}

    retval[self.heron_shell_ids[self.shard]] = Command([
        '%s' % self.heron_shell_binary,
        '--port=%s' % self.shell_port,
        '--log_file_prefix=%s/heron-shell-%s.log' % (self.log_dir, self.shard),
        '--secret=%s' % self.topology_id], self.shell_env)

    return retval