def _execute_wakeup_tasks(self):
    """Executes wakeup tasks, should only be called from loop()"""
    # Check the length of wakeup tasks first to avoid concurrent issues
    size = len(self.wakeup_tasks)
    for i in range(size):
      self.wakeup_tasks[i]()