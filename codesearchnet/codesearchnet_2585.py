def initialize(self, config, context):
    """Implements Pulsar Spout's initialize method"""
    self.logger.info("Initializing PulsarSpout with the following")
    self.logger.info("Component-specific config: \n%s" % str(config))
    self.logger.info("Context: \n%s" % str(context))

    self.emit_count = 0
    self.ack_count = 0
    self.fail_count = 0

    if not PulsarSpout.serviceUrl in config or not PulsarSpout.topicName in config:
      self.logger.fatal("Need to specify both serviceUrl and topicName")
    self.pulsar_cluster = str(config[PulsarSpout.serviceUrl])
    self.topic = str(config[PulsarSpout.topicName])
    mode = config[api_constants.TOPOLOGY_RELIABILITY_MODE]
    if mode == api_constants.TopologyReliabilityMode.ATLEAST_ONCE:
      self.acking_timeout = 1000 * int(config[api_constants.TOPOLOGY_MESSAGE_TIMEOUT_SECS])
    else:
      self.acking_timeout = 30000
    if PulsarSpout.receiveTimeoutMs in config:
      self.receive_timeout_ms = config[PulsarSpout.receiveTimeoutMs]
    else:
      self.receive_timeout_ms = 10
    if PulsarSpout.deserializer in config:
      self.deserializer = config[PulsarSpout.deserializer]
      if not callable(self.deserializer):
        self.logger.fatal("Pulsar Message Deserializer needs to be callable")
    else:
      self.deserializer = self.default_deserializer

    # First generate the config
    self.logConfFileName = GenerateLogConfig(context)
    self.logger.info("Generated LogConf at %s" % self.logConfFileName)

    # We currently use the high level consumer API
    # For supporting effectively once, we will need to switch
    # to using lower level Reader API, when it becomes
    # available in python
    self.client = pulsar.Client(self.pulsar_cluster, log_conf_file_path=self.logConfFileName)
    self.logger.info("Setup Client with cluster %s" % self.pulsar_cluster)
    try:
      self.consumer = self.client.subscribe(self.topic, context.get_topology_name(),
                                            consumer_type=pulsar.ConsumerType.Failover,
                                            unacked_messages_timeout_ms=self.acking_timeout)
    except Exception as e:
      self.logger.fatal("Pulsar client subscription failed: %s" % str(e))

    self.logger.info("Subscribed to topic %s" % self.topic)