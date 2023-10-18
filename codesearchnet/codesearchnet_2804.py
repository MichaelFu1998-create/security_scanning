def class_dict_to_specs(mcs, class_dict):
    """Takes a class `__dict__` and returns `HeronComponentSpec` entries"""
    specs = {}

    for name, spec in class_dict.items():
      if isinstance(spec, HeronComponentSpec):
        # Use the variable name as the specification name.
        if spec.name is None:
          spec.name = name
        if spec.name in specs:
          raise ValueError("Duplicate component name: %s" % spec.name)
        else:
          specs[spec.name] = spec
    return specs