def initialize(self, config, context):
    """We initialize the window duration and slide interval
    """
    if TumblingWindowBolt.WINDOW_DURATION_SECS in config:
      self.window_duration = int(config[TumblingWindowBolt.WINDOW_DURATION_SECS])
    else:
      self.logger.fatal("Window Duration has to be specified in the config")

    # By modifying the config, we are able to setup the tick timer
    config[api_constants.TOPOLOGY_TICK_TUPLE_FREQ_SECS] = str(self.window_duration)
    self.current_tuples = deque()
    if hasattr(self, 'saved_state'):
      if 'tuples' in self.saved_state:
        self.current_tuples = self.saved_state['tuples']