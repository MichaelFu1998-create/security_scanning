def _get_comp_config(self):
    """Returns component-specific Config protobuf message

    It first adds ``topology.component.parallelism``, and is overriden by
    a user-defined component-specific configuration, specified by spec().
    """
    proto_config = topology_pb2.Config()

    # first add parallelism
    key = proto_config.kvs.add()
    key.key = TOPOLOGY_COMPONENT_PARALLELISM
    key.value = str(self.parallelism)
    key.type = topology_pb2.ConfigValueType.Value("STRING_VALUE")

    # iterate through self.custom_config
    if self.custom_config is not None:
      sanitized = self._sanitize_config(self.custom_config)
      for key, value in sanitized.items():
        if isinstance(value, str):
          kvs = proto_config.kvs.add()
          kvs.key = key
          kvs.value = value
          kvs.type = topology_pb2.ConfigValueType.Value("STRING_VALUE")
        else:
          # need to serialize
          kvs = proto_config.kvs.add()
          kvs.key = key
          kvs.serialized_value = default_serializer.serialize(value)
          kvs.type = topology_pb2.ConfigValueType.Value("PYTHON_SERIALIZED_VALUE")

    return proto_config