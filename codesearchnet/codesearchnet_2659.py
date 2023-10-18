def process_tick(self, tup):
    """Called every slide_interval
    """
    curtime = int(time.time())
    window_info = WindowContext(curtime - self.window_duration, curtime)
    tuple_batch = []
    for (tup, tm) in self.current_tuples:
      tuple_batch.append(tup)
    self.processWindow(window_info, tuple_batch)
    self._expire(curtime)