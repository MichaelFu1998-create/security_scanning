def run(self):
    """
    Run the command, infer time period to be used in metric analysis phase.
    :return: None
    """
    cmd_args = shlex.split(self.run_cmd)
    logger.info('Local command RUN-STEP starting with rank %d', self.run_rank)
    logger.info('Running subprocess command with following args: ' + str(cmd_args))

    # TODO: Add try catch blocks. Kill process on CTRL-C
    # Infer time period for analysis. Assume same timezone between client and servers.
    self.ts_start = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
      self.process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
      if self.kill_after_seconds:
        self.timer = Timer(self.kill_after_seconds, self.kill)
        self.timer.start()
      # Using 2nd method here to stream output:
      # http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate
      for line in iter(self.process.stdout.readline, b''):
        logger.info(line.strip())
      self.process.communicate()
    except KeyboardInterrupt:
      logger.warning('Handling keyboard interrupt (Ctrl-C)')
      self.kill()
    if self.timer:
      self.timer.cancel()
    self.ts_end = time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info('subprocess finished')
    logger.info('run_step started at ' + self.ts_start + ' and ended at ' + self.ts_end)