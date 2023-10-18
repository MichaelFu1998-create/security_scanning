def _get_next_timeout_interval(self):
    """Get the next timeout from now

    This should be used from do_wait().
    :returns (float) next_timeout, or 10.0 if there are no timer events
    """
    if len(self.timer_tasks) == 0:
      return sys.maxsize
    else:
      next_timeout_interval = self.timer_tasks[0][0] - time.time()
      return next_timeout_interval