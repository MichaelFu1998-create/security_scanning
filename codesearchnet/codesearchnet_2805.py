def class_dict_to_topo_config(mcs, class_dict):
    """
    Takes a class `__dict__` and returns a map containing topology-wide
    configuration.

    The returned dictionary is a sanitized `dict` of type `<str ->
    (str|object)>`.

    This classmethod firsts insert default topology configuration and then
    overrides it with a given topology-wide configuration. Note that this
    configuration will be overriden by a component-specific configuration at
    runtime.
    """
    topo_config = {}

    # add defaults
    topo_config.update(mcs.DEFAULT_TOPOLOGY_CONFIG)

    for name, custom_config in class_dict.items():
      if name == 'config' and isinstance(custom_config, dict):
        sanitized_dict = mcs._sanitize_config(custom_config)
        topo_config.update(sanitized_dict)

    return topo_config