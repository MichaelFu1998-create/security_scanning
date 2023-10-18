def add_spec(self, *specs):
    """Add specs to the topology

    :type specs: HeronComponentSpec
    :param specs: specs to add to the topology
    """
    for spec in specs:
      if not isinstance(spec, HeronComponentSpec):
        raise TypeError("Argument to add_spec needs to be HeronComponentSpec, given: %s"
                        % str(spec))
      if spec.name is None:
        raise ValueError("TopologyBuilder cannot take a spec without name")
      if spec.name == "config":
        raise ValueError("config is a reserved name")
      if spec.name in self._specs:
        raise ValueError("Attempting to add duplicate spec name: %r %r" % (spec.name, spec))

      self._specs[spec.name] = spec