def initialize(self):
    """
    Initialize the environment. Done with a method call outside of the constructor for 2 reasons:
    1. Unit tests probably won't want/need to do this
    2. We don't initialize the logger (also something unit tests don't want) until after the
    constructor
    """
    create_folders = Command('mkdir -p %s' % self.log_dir, self.shell_env)
    self.run_command_or_exit(create_folders)

    chmod_logs_dir = Command('chmod a+rx . && chmod a+x %s' % self.log_dir, self.shell_env)
    self.run_command_or_exit(chmod_logs_dir)

    chmod_x_binaries = [self.tmaster_binary, self.stmgr_binary, self.heron_shell_binary]

    for binary in chmod_x_binaries:
      stat_result = os.stat(binary)[stat.ST_MODE]
      if not stat_result & stat.S_IXOTH:
        chmod_binary = Command('chmod +x %s' % binary, self.shell_env)
        self.run_command_or_exit(chmod_binary)

    # Log itself pid
    log_pid_for_process(get_heron_executor_process_name(self.shard), os.getpid())