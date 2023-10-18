def process_tick(self, tup):
    """Called every window_duration
    """
    curtime = int(time.time())
    window_info = WindowContext(curtime - self.window_duration, curtime)
    self.processWindow(window_info, list(self.current_tuples))
    for tup in self.current_tuples:
      self.ack(tup)
    self.current_tuples.clear()