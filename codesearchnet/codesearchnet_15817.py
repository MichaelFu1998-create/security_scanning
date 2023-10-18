def kill(self):
    """
    If run_step needs to be killed, this method will be called
    :return: None
    """
    try:
      logger.info('Trying to terminating run_step...')
      self.process.terminate()
      time_waited_seconds = 0
      while self.process.poll() is None and time_waited_seconds < CONSTANTS.SECONDS_TO_KILL_AFTER_SIGTERM:
        time.sleep(0.5)
        time_waited_seconds += 0.5
      if self.process.poll() is None:
        self.process.kill()
        logger.warning('Waited %d seconds for run_step to terminate. Killing now....', CONSTANTS.SECONDS_TO_KILL_AFTER_SIGTERM)
    except OSError, e:
      logger.error('Error while trying to kill the subprocess: %s', e)