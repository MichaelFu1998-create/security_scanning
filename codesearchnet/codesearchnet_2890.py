def _get_dict_from_config(topology_config):
    """Converts Config protobuf message to python dictionary

    Values are converted according to the rules below:

    - Number string (e.g. "12" or "1.2") is appropriately converted to ``int`` or ``float``
    - Boolean string ("true", "True", "false" or "False") is converted to built-in boolean type
      (i.e. ``True`` or ``False``)
    - Normal string is inserted to dict as is
    - Serialized value is deserialized and inserted as a corresponding Python object
    """
    config = {}
    for kv in topology_config.kvs:
      if kv.HasField("value"):
        assert kv.type == topology_pb2.ConfigValueType.Value("STRING_VALUE")
        # value is string
        if PhysicalPlanHelper._is_number(kv.value):
          config[kv.key] = PhysicalPlanHelper._get_number(kv.value)
        elif kv.value.lower() in ("true", "false"):
          config[kv.key] = True if kv.value.lower() == "true" else False
        else:
          config[kv.key] = kv.value
      elif kv.HasField("serialized_value") and \
        kv.type == topology_pb2.ConfigValueType.Value("PYTHON_SERIALIZED_VALUE"):
        # deserialize that
        config[kv.key] = default_serializer.deserialize(kv.serialized_value)
      else:
        assert kv.HasField("type")
        Log.error("Unsupported config <key:value> found: %s, with type: %s"
                  % (str(kv), str(kv.type)))
        continue

    return config