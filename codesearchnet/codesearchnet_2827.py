def _sanitize_config(custom_config):
    """Checks whether ``custom_config`` is sane and returns a sanitized dict <str -> (str|object)>

    It checks if keys are all strings and sanitizes values of a given dictionary as follows:

    - If string, number or boolean is given as a value, it is converted to string.
      For string and number (int, float), it is converted to string by a built-in ``str()`` method.
      For a boolean value, ``True`` is converted to "true" instead of "True", and ``False`` is
      converted to "false" instead of "False", in order to keep the consistency with
      Java configuration.

    - If neither of the above is given as a value, it is inserted into the sanitized dict as it is.
      These values will need to be serialized before adding to a protobuf message.
    """
    if not isinstance(custom_config, dict):
      raise TypeError("Component-specific configuration must be given as a dict type, given: %s"
                      % str(type(custom_config)))
    sanitized = {}
    for key, value in custom_config.items():
      if not isinstance(key, str):
        raise TypeError("Key for component-specific configuration must be string, given: %s:%s"
                        % (str(type(key)), str(key)))

      if isinstance(value, bool):
        sanitized[key] = "true" if value else "false"
      elif isinstance(value, (str, int, float)):
        sanitized[key] = str(value)
      else:
        sanitized[key] = value

    return sanitized