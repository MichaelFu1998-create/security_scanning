def component_id(self):
    """Returns component_id of this GlobalStreamId

    Note that if HeronComponentSpec is specified as componentId and its name is not yet
    available (i.e. when ``name`` argument was not given in ``spec()`` method in Bolt or Spout),
    this property returns a message with uuid. However, this is provided only for safety
    with __eq__(), __str__(), and __hash__() methods, and not meant to be called explicitly
    before TopologyType class finally sets the name attribute of HeronComponentSpec.
    """
    if isinstance(self._component_id, HeronComponentSpec):
      if self._component_id.name is None:
        # HeronComponentSpec instance's name attribute might not be available until
        # TopologyType metaclass finally sets it. This statement is to support __eq__(),
        # __hash__() and __str__() methods with safety, as raising Exception is not
        # appropriate this case.
        return "<No name available for HeronComponentSpec yet, uuid: %s>" % self._component_id.uuid
      return self._component_id.name
    elif isinstance(self._component_id, str):
      return self._component_id
    else:
      raise ValueError("Component Id for this GlobalStreamId is not properly set: <%s:%s>"
                       % (str(type(self._component_id)), str(self._component_id)))