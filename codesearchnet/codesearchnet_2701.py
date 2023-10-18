def _trigger_timers(self):
    """Triggers expired timers"""
    current = time.time()
    while len(self.timer_tasks) > 0 and (self.timer_tasks[0][0] - current <= 0):
      task = heappop(self.timer_tasks)[1]
      task()