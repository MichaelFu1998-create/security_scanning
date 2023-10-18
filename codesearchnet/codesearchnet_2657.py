def initialize(self, config, context):
    """We initialize the window duration and slide interval
    """
    if SlidingWindowBolt.WINDOW_DURATION_SECS in config:
      self.window_duration = int(config[SlidingWindowBolt.WINDOW_DURATION_SECS])
    else:
      self.logger.fatal("Window Duration has to be specified in the config")
    if SlidingWindowBolt.WINDOW_SLIDEINTERVAL_SECS in config:
      self.slide_interval = int(config[SlidingWindowBolt.WINDOW_SLIDEINTERVAL_SECS])
    else:
      self.slide_interval = self.window_duration
    if self.slide_interval > self.window_duration:
      self.logger.fatal("Slide Interval should be <= Window Duration")

    # By modifying the config, we are able to setup the tick timer
    config[api_constants.TOPOLOGY_TICK_TUPLE_FREQ_SECS] = str(self.slide_interval)
    self.current_tuples = deque()
    if hasattr(self, 'saved_state'):
      if 'tuples' in self.saved_state:
        self.current_tuples = self.saved_state['tuples']